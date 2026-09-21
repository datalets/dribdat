# Vibecoding Hackathons with Dribdat

This guide explains how **Dribdat** enables **Vibecoding Hackathons**—events where participants build software primarily through prompt-driven interactions with AI chatbots, coding assistants, and autonomous agents (such as Cursor, Claude Desktop, GitHub Copilot, ChatGPT, or custom LLM scripts).

---

## What is Vibecoding in a Hackathon?

In a traditional hackathon, progress is committed to version control or documented manually on project boards. In a **vibecoding hackathon**, developers collaborate tightly with LLM agents to rapidly prototype solutions, iterate on code, and refine architecture.

However, rapid prompt-based development often creates a visibility problem: critical decisions, creative prompts, and debugging sessions remain hidden inside local IDE chats or browser windows.

**Dribdat solves this by serving as a central event heartbeat.** Through its Model Context Protocol (**MCP**) server integration, Dribdat allows AI assistants and background agents to seamlessly post updates directly to the project log while developers remain focused on coding.

---

## Architecture Overview: MCP Integration

Dribdat implements a [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server endpoint using the official Python MCP SDK. This enables any MCP-compliant client or AI agent to read event context, search projects, and write updates back to the hackathon project log.

```
+---------------------+           +------------------------+           +------------------+
|  Developer + AI     |  MCP SSE  |     Dribdat Platform   |  Public   | Hackathon Audience|
| (Cursor/Claude/...) | --------> | /api/mcp/sse & messages| --------> | & Event Timeline |
+---------------------+           +------------------------+           +------------------+
```

### Authentication & Token Workflow

1. Each registered user can generate a unique, non-expiring `mcp_token`.
2. Access your token at **User Profile > Edit Profile > Connect to MCP** (`/mcp/auth`).
3. Pass this token when establishing an MCP connection via Server-Sent Events (SSE) or HTTP headers.

---

## Built-In MCP Tools

The Dribdat MCP server exposes tools for reading state and logging updates:

### Read Operations
- **`get_event_info(event_id: int = None)`**
  Retrieves event metadata, schedule, and current status. Defaults to the active event.
- **`search_projects(query: str, event_id: int = None)`**
  Searches projects by keyword, returning matching titles, summaries, and tags.
- **`get_project_details(project_id: int)`**
  Fetches detailed project information, pitch, autotext, and current phase.
- **`get_activities(project_id: int = None, limit: int = 10)`**
  Fetches recent activity feed entries / posts for an event or specific project.

### Write Operations
- **`add_post(project_id: int, text: str)`**
  Posts a new update/drib to the project timeline. Used by agents to record chatbot summaries, key code iterations, or architectural decisions.
- **`update_project_status(project_id: int)`**
  Promotes the project to its next stage in the hackathon lifecycle (e.g., from Idea to Prototype).

---

## Configuring AI Assistants & IDEs

### 1. Connecting Claude Desktop / Cursor

Add the Dribdat MCP SSE endpoint to your MCP client configuration file (e.g., `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "dribdat": {
      "url": "https://your-dribdat-instance.org/api/mcp/sse?token=YOUR_MCP_TOKEN",
      "transport": "sse"
    }
  }
}
```

### 2. System Instructions for AI Agents

Give your AI assistant instructions on when and how to post updates to Dribdat. Add a rule to your repository's `.cursorrules`, `SYSTEM_PROMPT`, or custom agent instructions:

> **System Instruction for Agent:**
> "You are participating in a hackathon hosted on Dribdat. Our Project ID is `<PROJECT_ID>`.
> Whenever we reach a milestone (e.g., completing a feature, resolving a major bug, changing tech stack, or finalizing a prompt workflow), summarize what was accomplished in 2-3 concise bullet points and call the `add_post` tool on the Dribdat server."

---

## Automated Interaction Logging Recipes

### Recipe: Python Background Logger for Chatbot Sessions

If you run local LLM sessions or scripts, you can run a background script that posts interaction digests to Dribdat periodically using HTTP POST:

```python
import requests

MCP_MESSAGES_URL = "https://your-dribdat-instance.org/api/mcp/messages?token=YOUR_MCP_TOKEN"
PROJECT_ID = 42

def log_vibecoding_session(summary_text: str):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "add_post",
            "arguments": {
                "project_id": PROJECT_ID,
                "text": f"🤖 **Vibecoding Update**\n\n{summary_text}"
            }
        }
    }
    response = requests.post(MCP_MESSAGES_URL, json=payload)
    print("Logged to Dribdat:", response.json())

# Example invocation
if __name__ == "__main__":
    summary = (
        "- Generated Flask authentication routes using Claude 3.7 Sonnet.\n"
        "- Resolved database migration lock issue.\n"
        "- Verified unit tests pass with 95% coverage."
    )
    log_vibecoding_session(summary)
```

---

## Event Organizing Guide for Vibecoding Hackathons

### Pre-Event Setup
1. **Enable MCP Support:** Ensure your Dribdat instance is running with MCP blueprint registered.
2. **Provide Token Guide:** Instruct participants to retrieve their MCP token from `/mcp/auth`.
3. **Template Prompts:** Provide participants with starter `.cursorrules` or system prompt templates for their AI agents.

### During the Event
- **Live Activity Feed:** Display the Dribdat live activity dashboard on stage or in online streams to showcase real-time AI-human co-creation updates.
- **Stage Progression:** Use the `update_project_status` tool or manual progression to guide projects through *Idea*, *Wireframe*, *Prototype*, and *Presentation* stages.

### Judging & Showcase
- **Transparent Auditing:** Judges can inspect the project timeline to review the prompt history, agent contributions, and human oversight throughout the event.
