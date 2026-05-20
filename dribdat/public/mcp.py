import uuid
import json
import asyncio
import logging
import time
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    jsonify,
    current_app,
    Response,
    stream_with_context
)
from flask_login import login_required, current_user
from mcp.server.fastmcp import FastMCP
from mcp.shared.exceptions import McpError
import mcp.types as types
from ..user.models import Event, Project, Activity, User
from ..database import db
from ..utils import markdownit
from ..public.projhelper import project_action
from ..user.constants import PR_CHALLENGE
from ..user import stageProjectToNext

blueprint = Blueprint("mcp", __name__)

# Initialize FastMCP server
mcp_server = FastMCP("Dribdat")

# --- MCP Tools ---

@mcp_server.tool()
def get_event_info(event_id: int = None):
    """Get information about a specific event or the current one."""
    if event_id:
        event = Event.query.get(event_id)
    else:
        event = Event.query.filter_by(is_current=True).first() or \
                Event.query.order_by(Event.id.desc()).first()

    if not event:
        return "No event found."

    return json.dumps(event.get_full_data(), default=str)

@mcp_server.tool()
def search_projects(query: str, event_id: int = None):
    """Search for projects matching a query string."""
    q = Project.query.filter(Project.is_hidden == False)
    if event_id:
        q = q.filter_by(event_id=event_id)

    search_query = f"%{query}%"
    projects = q.filter(
        (Project.name.ilike(search_query)) |
        (Project.summary.ilike(search_query)) |
        (Project.longtext.ilike(search_query))
    ).all()

    return json.dumps([p.data for p in projects], default=str)

@mcp_server.tool()
def get_project_details(project_id: int):
    """Get full details of a project by ID."""
    project = Project.query.get(project_id)
    if not project:
        return "Project not found."

    data = project.data
    data['longtext'] = project.longtext
    data['autotext'] = project.autotext
    return json.dumps(data, default=str)

@mcp_server.tool()
def get_activities(project_id: int = None, limit: int = 10):
    """Get recent activities/posts, optionally filtered by project."""
    q = Activity.query
    if project_id:
        q = q.filter_by(project_id=project_id)

    activities = q.order_by(Activity.timestamp.desc()).limit(limit).all()
    return json.dumps([a.data for a in activities], default=str)

@mcp_server.tool()
def add_post(project_id: int, text: str):
    """Add a new post/update to a project."""
    # Note: Authentication context is handled via the transport/token
    user = getattr(request, 'mcp_user', None)
    if not user:
        return "Error: MCP session not authenticated."

    project = Project.query.get(project_id)
    if not project:
        return "Error: Project not found."

    project_action(project.id, "update", action="post", text=text, for_user=user)
    return f"Post added to project '{project.name}'."

@mcp_server.tool()
def update_project_status(project_id: int):
    """Promote a project to the next stage/level."""
    user = getattr(request, 'mcp_user', None)
    if not user:
        return "Error: MCP session not authenticated."

    project = Project.query.get(project_id)
    if not project:
        return "Error: Project not found."

    # Check if user is allowed to edit
    if not user.is_admin and project.user_id != user.id:
        # Check if user has starred (joined) the project
        starred = Activity.query.filter_by(
            name='star', project_id=project.id, user_id=user.id
        ).first()
        if not starred:
            return "Error: You do not have permission to update this project."

    if stageProjectToNext(project):
        project.update_now()
        db.session.add(project)
        db.session.commit()
        return f"Project '{project.name}' promoted to stage '{project.phase}'."
    else:
        return f"Project '{project.name}' is already at the maximum stage or not ready for promotion."

# --- MCP Blueprint Routes ---

@blueprint.route("/mcp/auth")
@login_required
def mcp_auth():
    """Page for user to get their one-time MCP token."""
    if not current_user.mcp_token:
        current_user.mcp_token = str(uuid.uuid4())
        db.session.add(current_user)
        db.session.commit()
    return render_template("public/mcp_auth.html", token=current_user.mcp_token)

@blueprint.route("/api/mcp/sse")
def mcp_sse():
    """SSE endpoint for MCP."""
    token = request.args.get("token")
    user = User.query.filter_by(mcp_token=token).first()
    if not user:
        return "Unauthorized", 401

    def event_stream():
        # First message is the endpoint for client-to-server messages
        msg_url = url_for(".mcp_messages", token=token, _external=True)
        yield f"event: endpoint\ndata: {msg_url}\n\n"

        while True:
            time.sleep(30)
            yield ": keep-alive\n\n"

    return Response(stream_with_context(event_stream()), mimetype="text/event-stream")

@blueprint.route("/api/mcp/messages", methods=["POST"])
def mcp_messages():
    """Endpoint for client-to-server messages."""
    token = request.args.get("token")
    user = User.query.filter_by(mcp_token=token).first()
    if not user:
        return "Unauthorized", 401

    # Attach user to request for tools to use
    request.mcp_user = user

    payload = request.get_json()
    method = payload.get('method')
    params = payload.get('params', {})
    request_id = payload.get('id')

    try:
        if method == "initialize":
            result = {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "Dribdat",
                    "version": "0.1.0"
                }
            }
            return jsonify({"jsonrpc": "2.0", "id": request_id, "result": result})

        elif method == "tools/list":
            tools_list = []
            for name, tool in mcp_server._tool_manager.list_tools():
                tools_list.append({
                    "name": name,
                    "description": tool.description,
                    "inputSchema": tool.parameters.model_json_schema()
                })
            return jsonify({"jsonrpc": "2.0", "id": request_id, "result": {"tools": tools_list}})

        elif method == "tools/call":
            tool_name = params.get('name')
            tool_args = params.get('arguments', {})

            # Lookup the tool and call it
            tool = next((t for n, t in mcp_server._tool_manager.list_tools() if n == tool_name), None)
            if not tool:
                return jsonify({"jsonrpc": "2.0", "id": request_id, "error": {"code": -32601, "message": "Tool not found"}})

            # Execute tool (FastMCP tools can be sync or async)
            import inspect
            if inspect.iscoroutinefunction(tool.fn):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                res_content = loop.run_until_complete(tool.fn(**tool_args))
            else:
                res_content = tool.fn(**tool_args)

            return jsonify({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [{"type": "text", "text": str(res_content)}]
                }
            })

        return jsonify({"jsonrpc": "2.0", "id": request_id, "error": {"code": -32601, "message": "Method not found"}})
    except Exception as e:
        current_app.logger.error(f"MCP Error: {str(e)}")
        return jsonify({"jsonrpc": "2.0", "id": request_id, "error": {"code": -32603, "message": str(e)}})
