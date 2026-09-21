# Devora

> **Your personal intelligence platform.**

Devora is an extensible personal intelligence platform that collects, analyzes, and organizes a user's digital activities to provide personalized insights, recommendations, planning, and automation.

The platform is designed with a modular backend so new capabilities can be added independently without restructuring the existing system.

The first major module is **DSA Intelligence**, which tracks coding activity across platforms such as LeetCode, Codeforces, and GeeksforGeeks, analyzes problem-solving performance, identifies weak topics, recommends problems, manages revision, and generates personalized study plans.

The architecture is intentionally designed to support future modules such as:
- Habit tracking
- Digital activity tracking
- Productivity analytics
- Personal planning
- Learning analytics
- Goal tracking
- AI-powered personal assistance
- Additional platform integrations

All modules share common infrastructure such as authentication, users, database access, security, background processing, and AI capabilities while remaining independently organized.

---

## Table of Contents

- [Overview](#overview)
- [Why Devora?](#why-devora)
- [Core Philosophy](#core-philosophy)
- [Architecture](#architecture)
- [Modular Architecture](#modular-architecture)
- [Current Modules](#current-modules)
  - [DSA Intelligence](#dsa-intelligence)
- [Future Modules](#future-modules)
  - [Habit Tracking](#habit-tracking)
  - [Digital Activity](#digital-activity)
  - [Productivity](#productivity)
  - [Goal Tracking](#goal-tracking)
- [Core Features](#core-features)
- [DSA Intelligence](#dsa-intelligence-1)
- [Authentication](#authentication)
- [AI & MCP](#ai--mcp)
- [Chrome Extension](#chrome-extension)
- [Database Architecture](#database-architecture)
- [Backend Architecture](#backend-architecture)
- [Frontend Architecture](#frontend-architecture)
- [Project Structure](#project-structure)
- [Local Development](#local-development)
- [Environment Variables](#environment-variables)
- [API Structure](#api-structure)
- [Security](#security)
- [Development Roadmap](#development-roadmap)
- [Future Vision](#future-vision)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Most users manage their digital activities across fragmented platforms without a unified intelligence layer.

Devora brings all these streams together into a single modular platform:
1. **DSA Intelligence**: Tracks competitive programming across LeetCode, Codeforces, and GeeksforGeeks, analyzing progress, weak topics, and study schedules.
2. **Personal Intelligence**: Extends data collection and analysis to habits, productivity, and digital activity.

---

## Why Devora?

Without a unified intelligence platform, data remains isolated in silos. 

Devora transforms scattered raw user activity into actionable insights, structured recommendations, and automated study or productivity plans.

---

## Core Philosophy

Devora follows a simple principle:

$$\text{Collect} \longrightarrow \text{Understand} \longrightarrow \text{Recommend} \longrightarrow \text{Plan} \longrightarrow \text{Act}$$

1. **Collect**: Automatically gather activity data (e.g., via Chrome extensions, webhooks, or API integrations).
2. **Understand**: Analyze patterns, measure performance, and detect weak spots.
3. **Recommend**: Suggest next actions, topics to revise, or habits to form.
4. **Plan**: Build personalized daily schedules and study plans.
5. **Act**: Enable AI agents (via MCP) to execute tasks, send notifications, or automate workflows.

---

## Architecture

Devora follows a modular monolith architecture initially. This provides the simplicity of a single backend while keeping individual features isolated enough to evolve independently.

```text
                         DEVORA
                            │
             ┌──────────────┼──────────────┐
             │              │              │
          Web App       Mobile App     Extensions
             │              │              │
             └──────────────┼──────────────┘
                            ↓
                    FastAPI Backend
                            │
              ┌─────────────┴─────────────┐
              │                           │
        Shared Infrastructure          Modules
              │                           │
      ┌───────┼────────┐        ┌─────────┼─────────┐
      │       │        │        │         │         │
     Auth   Security   DB       DSA     Habits    Future
                                  │
                                  ↓
                            Intelligence
                               Engine
                                  │
                                  ↓
                              MCP / AI
```

---

## Modular Architecture

### Design Goal

A new feature should ideally be added as a new module rather than requiring changes throughout the existing application.

```text
Add Habit Tracking
       ↓
Create habits module
       ↓
Add models
       ↓
Add APIs
       ↓
Add services
       ↓
Connect to shared authentication
       ↓
Feature becomes available to Web/Mobile/AI
```

This allows Devora to grow from a DSA assistant into a broader personal intelligence platform without rewriting core architecture.

### Module Independence Rules

1. **Independent Boundaries**: Each Devora feature should be implemented as an independent module with clear boundaries. Modules may use shared infrastructure and user identity, but one module should not tightly depend on the internal implementation of another module.
2. **Stable Interfaces**: Modules must depend on shared infrastructure through stable interfaces, not on the internal implementation of other modules. Cross-module communication should occur through public services, schemas, or well-defined interfaces.

---

## Current Modules

### DSA Intelligence
Tracks coding activity across LeetCode, Codeforces, and GeeksforGeeks, analyzes problem-solving performance, identifies weak topics, recommends problems, manages revision schedules, and generates personalized study plans.

---

## Future Modules

### Habit Tracking
Track daily habits, streak maintenance, and behavioral consistency across routines.

### Digital Activity
Monitor digital surface activity, active application time, and contextual workflow state.

### Productivity
Analyze focus blocks, task completion rates, and daily focus scores.

### Goal Tracking
Set long-term milestones, track progress velocity, and decompose goals into daily actions.

---

## Core Features

- **Centralized Data Aggregation**: Sync problem-solving activity across multiple platforms.
- **Topic & Skill Weakness Analysis**: Identify topic-specific accuracy and submission cadence.
- **Smart Revision Scheduler**: Spaced-repetition scheduling for previously solved problems.
- **Personalized Recommendations**: Context-aware problem suggestions based on current weak points.
- **Extensible AI Capabilities**: Model Context Protocol (MCP) server integration allowing AI assistants to query performance and suggest study plans.

---

## DSA Intelligence

The DSA Intelligence engine consists of 6 sub-domains:
- **Problems**: Aggregates platform definitions, problems, and topic mappings.
- **Submissions**: Records submission logs, execution times, memory usage, and difficulty.
- **Progress**: Computes topic accuracy, difficulty distribution, and daily streaks.
- **Recommendations**: Generates recommended problem sets tailored to user gaps.
- **Revision**: Manages spaced repetition queues for problem re-solving.
- **Scheduler**: Builds customized study plans and calendar routines.

---

## Authentication

Devora uses a secure JWT-based authentication system backed by PostgreSQL:
- Local signup/login with hashed passwords (`bcrypt` / `passlib`)
- Access tokens (short-lived) & Refresh tokens (long-lived)
- Future support for Google OAuth & OTP email verification

---

## AI & MCP

Devora integrates with Model Context Protocol (MCP) to expose tool endpoints for LLM assistants (e.g. Claude, Gemini, Antigravity Agent):
- Query current DSA stats and weak topics
- Generate dynamic study recommendations
- Automate task tracking and plan generation

---

## Chrome Extension

The Devora Chrome Extension runs in the background to automatically capture submission details from supported platforms (LeetCode, Codeforces, GFG) without manual data entry.

---

## Database Architecture

Devora uses PostgreSQL managed via SQLAlchemy 2.0 ORM and Alembic migrations.

Shared tables:
- `users`: Core identity, email, authentication details.

DSA Module tables:
- `platforms`: Platform definitions (LeetCode, Codeforces, GeeksforGeeks)
- `topics`: Master topic taxonomy (Graphs, Dynamic Programming, Trees, etc.)
- `problems`: Unique problem records across platforms
- `problem_topics`: Many-to-many relationship mapping problems to topics
- `submissions`: User submission records with execution metadata

---

## Backend Architecture

Built with Python 3.11+ and FastAPI using modular monolith principles:

- `core/`: Application settings, security utilities (hashing, JWT), and authentication dependencies.
- `db/`: Database configuration, SQLAlchemy engine, `Base`, and session management (`get_db`).
- `modules/`: Feature modules (`auth`, `users`, `dsa`, etc.) encapsulating domain logic.
- `shared/`: Common response models, exception classes, and pagination utilities.

---

## Frontend Architecture

The frontend is built with React, Vite, and modern styling (Vanilla CSS with CSS variables and responsive glassmorphism design), designed to provide real-time charts, progress dashboards, and interactive study planners.

---

## Project Structure

```text
Devora/
├── backend/
│   ├── alembic/              # Database migration scripts
│   ├── app/
│   │   ├── core/             # Configuration & security dependencies
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── oauth.py
│   │   │   └── dependencies.py
│   │   ├── db/               # Database engine & session setup
│   │   │   └── database.py
│   │   ├── modules/          # Domain feature modules
│   │   │   ├── auth/         # Authentication endpoints & schemas
│   │   │   ├── users/        # User domain models
│   │   │   └── dsa/          # DSA Intelligence module
│   │   │       ├── problems/
│   │   │       └── submissions/
│   │   ├── shared/           # Cross-module helpers, exceptions, pagination
│   │   │   ├── exceptions.py
│   │   │   ├── pagination.py
│   │   │   └── responses.py
│   │   └── main.py           # FastAPI entrypoint
│   └── requirements.txt
├── frontend/                 # React + Vite web dashboard
├── extension/                # Browser Extension for automatic tracking
├── mcp-server/               # Model Context Protocol server
├── docker-compose.yml
└── README.md
```

---

## Local Development

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Node.js 18+ (for frontend/extension)

### Setup Backend

1. Navigate to backend:
   ```bash
   cd backend
   ```
2. Create virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Set environment variables in `.env` (see `.env.example`).
4. Run migrations:
   ```bash
   alembic upgrade head
   ```
5. Start dev server:
   ```bash
   uvicorn app.main:app --reload
   ```

---

## Environment Variables

Copy `.env.example` to `backend/.env`:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/devora_db
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

## API Structure

All API routes follow the `/api/<module>` prefix:

- `/api/auth/signup` - Register a new user
- `/api/auth/login` - Authenticate user & issue tokens
- `/api/auth/refresh` - Refresh access token

---

## Security

- Passwords hashed with `bcrypt`.
- JWT authentication with separate access and refresh tokens.
- CORS restricted to configured origins.
- Shared security utilities isolated in `app/core/security.py`.

---

## Development Roadmap

- **Phase 1 — Foundation**
  - Project setup, PostgreSQL schema design, base FastAPI setup, Docker configuration.
- **Phase 2 — Authentication**
  - JWT signup/login/refresh flow, password hashing, Google OAuth, OTP verification.
- **Phase 3 — DSA Intelligence**
  - Problem tracking, submission logging, topic breakdown, user stats calculation.
- **Phase 4 — Platform Integrations**
  - Chrome Extension background sync for LeetCode, Codeforces, and GeeksforGeeks.
- **Phase 5 — Recommendation & Intelligence Engine**
  - Weak topic identification, revision spaced repetition, automated study plan generation.
- **Phase 6 — MCP & AI Assistant**
  - Expose Model Context Protocol tools for AI assistant integrations.
- **Phase 7 — Production Infrastructure**
  - CI/CD, deployment configuration, monitoring, caching with Redis.
- **Phase 8 — Additional Modules**
  - Habit Tracking, Digital Activity Tracking, Productivity Analytics, Goal Tracking, Personal Analytics.

---

## Future Vision

Devora aims to become the definitive personal intelligence layer—empowering users to turn raw daily effort into structured growth across learning, habits, and career performance.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for improvements.

---

## License

[MIT](LICENSE)
