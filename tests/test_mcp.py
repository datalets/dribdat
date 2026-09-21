# -*- coding: utf-8 -*-
"""Test MCP endpoints and tools."""

import json
from dribdat.user.models import User, Event, Project, Activity
from .factories import UserFactory, EventFactory, ProjectFactory


class TestMCP:
    """Test MCP endpoints and functionality."""

    def test_mcp_auth_page_requires_login(self, testapp, db):
        """Test that /mcp/auth redirects unauthenticated users."""
        res = testapp.get("/mcp/auth")
        assert res.status_code == 302

    def test_mcp_auth_page(self, testapp, user):
        """Test user mcp_token generation and mcp_auth page."""
        res = testapp.get("/login/")
        form = res.forms["loginForm"]
        form["username"] = user.username
        form["password"] = "myprecious"
        res = form.submit().follow()

        res = testapp.get("/mcp/auth")
        assert res.status_code == 200
        assert "MCP Authentication" in res.text

        # Verify mcp_token was generated
        u = User.query.get(user.id)
        assert u.mcp_token is not None
        assert u.mcp_token in res.text

    def test_mcp_sse_unauthorized(self, testapp, db, user):
        """Test MCP SSE endpoint returns 401 without valid token or when token is missing/empty."""
        # User exists in DB with mcp_token=None
        assert user.mcp_token is None

        # Request with invalid token
        res = testapp.get("/api/mcp/sse?token=invalid", expect_errors=True)
        assert res.status_code == 401

        # Request with missing token parameter
        res = testapp.get("/api/mcp/sse", expect_errors=True)
        assert res.status_code == 401

        # Request with empty token parameter
        res = testapp.get("/api/mcp/sse?token=", expect_errors=True)
        assert res.status_code == 401

    def test_mcp_messages_unauthorized(self, testapp, db, user):
        """Test MCP messages endpoint returns 401 when token is missing or empty."""
        assert user.mcp_token is None
        payload = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}

        res = testapp.post_json("/api/mcp/messages", payload, expect_errors=True)
        assert res.status_code == 401

        res = testapp.post_json("/api/mcp/messages?token=", payload, expect_errors=True)
        assert res.status_code == 401

    def test_mcp_messages_initialize(self, testapp, user):
        """Test MCP messages initialization with valid token."""
        user.mcp_token = "test-mcp-token-123"
        user.save()

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {}
        }

        res = testapp.post_json(
            "/api/mcp/messages?token=test-mcp-token-123",
            payload
        )
        assert res.status_code == 200
        data = res.json
        assert data["result"]["serverInfo"]["name"] == "Dribdat"

    def test_mcp_messages_tools_list(self, testapp, user):
        """Test MCP listing tools."""
        user.mcp_token = "test-mcp-token-123"
        user.save()

        payload = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }

        res = testapp.post_json(
            "/api/mcp/messages?token=test-mcp-token-123",
            payload
        )
        assert res.status_code == 200
        tools = res.json["result"]["tools"]
        tool_names = [t["name"] for t in tools]
        assert "add_post" in tool_names
        assert "get_event_info" in tool_names
        assert "search_projects" in tool_names

    def test_mcp_call_add_post(self, testapp, user, project):
        """Test calling add_post tool via MCP messages."""
        user.mcp_token = "test-mcp-token-123"
        user.save()

        payload = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "add_post",
                "arguments": {
                    "project_id": project.id,
                    "text": "Hello from MCP agent!"
                }
            }
        }

        res = testapp.post_json(
            "/api/mcp/messages?token=test-mcp-token-123",
            payload
        )
        assert res.status_code == 200
        assert "Post added to project" in res.json["result"]["content"][0]["text"]

        # Check activity was logged
        activities = Activity.query.filter_by(project_id=project.id).all()
        assert len(activities) > 0
        assert "Hello from MCP agent!" in activities[0].content
