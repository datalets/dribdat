# Dribdat Modernization Proposal (vNext)

This document outlines a major rework of the Dribdat tech stack to modernize the application, improve developer and user experience, and ensure the codebase is optimized for **agentic development**.

## 1. Vision & Goals
- **Streamline Modern Hackathons:** Refocus on recommending bootstraps, collecting challenges/results, and supporting "vibe coding."
- **Agent-Friendly Codebase:** Architecture designed to be easily understood and modified by AI coding assistants.
- **Lightweight & Sustainable:** Minimize resource footprint, maximize portability, and keep hosting costs low.
- **Data Portability:** Use open standards like Frictionless Data Packages for all migrations and exports.

## 2. Modernized Tech Stack

### Backend: FastAPI
- **Language:** Python 3.12+
- **Framework:** FastAPI
- **Why:** High performance, native support for asynchronous programming, and automatic OpenAPI generation.
- **Agent Advantage:** Strict typing with Pydantic makes the API self-documenting for AI agents.

### Data Layer: SQLModel
- **ORM:** SQLModel (SQLAlchemy + Pydantic)
- **Database:** PostgreSQL (Production), SQLite (Development/Edge)
- **Why:** Reduces boilerplate by using the same models for database schemas and API responses.
- **Agent Advantage:** Single source of truth for data structures prevents "hallucinations" about model fields.

### Frontend: Vue.js 3 (Integrated Backboard)
- **Framework:** Vue 3 + Vite
- **UI Component Library:** Tailwind CSS (replaces Bootstrap for better customizability and smaller bundles)
- **Why:** Real-time interactivity for "Dribs" (activity logs) and a modern presentation mode.
- **Integration:** Merge the existing "Backboard" frontend into the core project.

### Storage & Media
- **Service:** S3-compatible storage (via `aioboto3`)
- **Use Case:** Project images, logos, and presentation uploads.

---

## 3. Agentic Development Process

To make the codebase "conducive to the use of agentic development," we recommend the following process and structure:

### Modular "Domain" Directory Structure
Instead of a monolithic `models.py` or `views.py`, the app should be organized by domain:
```text
dribdat_vnext/
├── domains/
│   ├── event/        # Models, Services, API routes for Events
│   │   ├── models.py
│   │   ├── service.py
│   │   ├── router.py
│   │   └── AGENTS.md # Specific instructions for AI agents working here
│   ├── project/      # Project management & Syncing
│   ├── user/         # Auth & Profiles
│   └── activity/     # Dribs & Logs
├── core/             # Base configurations, DB setup, generic utils
└── main.py           # Application entry point
```

### Strict Coding Standards
1. **100% Type Coverage:** Every function must have type hints for arguments and return values.
2. **Pydantic for Data Validation:** All external data must be validated through Pydantic schemas.
3. **Explicit Side Effects:** Business logic should reside in "Service" layers, keeping Routers (API endpoints) thin.
4. **AGENTS.md Files:** Each module contains an `AGENTS.md` file explaining its purpose, key patterns, and "gotchas."

---

## 4. Full Set of Requirements for Dribdat vNext

### R1: Core Event Management
- Ability to create, manage, and archive hackathon events.
- Support for "Phases" (Draft, Active, Finished).
- Customizable Event CSS and branding.
- Countdown timers and real-time announcements.

### R2: Project & Team Formation
- 7-Stage Project Lifecycle (Challenge -> ... -> Result).
- "Join" and "Star" functionality for team formation.
- **Bootstrap Recommendation Engine:** Organizers can tag projects as "Starters" or "Bootstraps" to guide participants.
- Support for "Vibe Coding" through simple, low-friction project updates.

### R3: Intelligent Data Sync (The "Sync Engine")
- Asynchronous synchronization of project metadata from:
    - GitHub (Repositories & Gists)
    - GitLab
    - Codeberg
    - HuggingFace
    - Etherpad
- Support for custom "Data Package" descriptors for project metadata.

### R4: Real-time Activity Log ("Dribs")
- A global and project-specific "firehose" of activity.
- Support for WebSockets or Server-Sent Events (SSE) to provide instant updates.
- Commenting and upvoting ("Boosting") features.

### R5: Presentation Mode
- Integrated slide mode using Markdown (Marpit compatible).
- Auto-embedding of external presentation links (Google Slides, Speaker Deck).
- Integrated timer and navigation for project showcases.

### R6: Data Portability & Migration
- Support for **Frictionless Data Package** (CSV/JSON) for exporting all event data.
- Migration scripts to import data from legacy Dribdat (Flask) instances.
- "Simple Resume" support via JSON-LD in user profiles.

---

## 5. Migration Strategy

1. **Export:** Use the existing Dribdat API to export data into a standard Data Package format.
2. **Schema Mapping:** Map legacy SQLAlchemy models to new SQLModel classes.
3. **Import:** Create a CLI tool in vNext that reads the Data Package and populates the new PostgreSQL database.
4. **Proxy/Co-existence:** (Optional) Run the legacy app in read-only mode for historical events while using vNext for new events.
