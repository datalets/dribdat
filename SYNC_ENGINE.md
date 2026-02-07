# Dribdat vNext: Project Sync Engine Redesign

The Project Sync Engine is responsible for aggregating data from various external sources (GitHub, GitLab, etc.) into the Dribdat project dashboard.

## 1. Current Architecture
Currently, synchronization is synchronous and happens during web requests or via simple CLI commands. It uses multiple libraries (`requests`, `pyquery`, etc.) and lacks a standardized plugin system.

## 2. Proposed vNext Architecture

### Asynchronous & Task-Based
Syncing should be non-blocking and managed by a task queue:
- **FastAPI BackgroundTasks** for simple, immediate syncs.
- **Taskiq** or **Celery** for scheduled or high-volume syncs.

### Provider-Based Plugin System
Each external data source should be a "Provider" class implementing a standard interface:

```python
class BaseProvider(ABC):
    @abstractmethod
    async def fetch_metadata(self, url: str) -> ProjectMetadata:
        """Fetch basic info: name, summary, image, etc."""
        pass

    @abstractmethod
    async def fetch_content(self, url: str) -> str:
        """Fetch long-form content (README.md)."""
        pass

    @abstractmethod
    async def fetch_activity(self, url: str, since: datetime) -> List[Activity]:
        """Fetch recent commits/updates."""
        pass
```

### Supported Providers (Priority)
1. **GitHub Provider:** Uses GitHub API (with optional token support to avoid rate limiting).
2. **GitLab Provider:** Supports both gitlab.com and self-hosted instances.
3. **HuggingFace Provider:** Syncs model/dataset cards.
4. **Codeberg/Gitea Provider:** Generic Forgejo/Gitea support.
5. **Generic Web/OpenGraph Provider:** Fallback for any URL (extracting Title, Description, and OG images).

## 3. Data Flow

1. **Trigger:** A user clicks "Sync", or a scheduled job runs.
2. **Dispatch:** The Sync Engine identifies the provider based on the `autotext_url`.
3. **Fetch:** The provider fetches data asynchronously.
4. **Transform:** Raw data is transformed into Pydantic models (e.g., `SyncData`).
5. **Reconcile:**
    - If a field is empty in Dribdat but present in the remote source, it is filled.
    - If a field is marked as "Always Sync," it is overwritten.
    - Commits are added as `Activity` objects if they don't already exist.
6. **Notify:** The user is notified via WebSocket/SSE that the sync is complete.

## 4. Agentic Advantage
- **Separation of Concerns:** Agents can easily implement new providers by following the `BaseProvider` interface without touching the core engine logic.
- **Mocking:** The standard interface makes it trivial to write unit tests with mocked network responses.
- **Type Safety:** Using Pydantic for the `ProjectMetadata` ensures that the transformation logic is robust and easy for agents to validate.
