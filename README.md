# Devora

> **Your DSA journey, intelligently managed.**

Devora is an AI-powered DSA progress tracking and personalized study assistant that helps developers track coding activity across multiple competitive programming platforms, understand their strengths and weaknesses, receive personalized problem recommendations, manage revisions, and generate optimized study plans.

Devora integrates with:

* LeetCode
* Codeforces
* GeeksforGeeks

It automatically tracks coding activity through a Chrome extension and provides a centralized dashboard for analyzing progress.

The long-term goal of Devora is to combine **DSA tracking + analytics + personalized recommendations + intelligent scheduling + MCP + LLMs** into one platform.

---

## Table of Contents

- [Overview](#overview)
- [Why Devora](#why-devora)
- [Core Features](#core-features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Application Flow](#application-flow)
- [Authentication](#authentication)
- [DSA Tracking](#dsa-tracking)
- [Progress Engine](#progress-engine)
- [Recommendation Engine](#recommendation-engine)
- [Revision Engine](#revision-engine)
- [Study Scheduler](#study-scheduler)
- [Chrome Extension](#chrome-extension)
- [MCP Server](#mcp-server)
- [Database Design](#database-design)
- [API Structure](#api-structure)
- [Local Development Setup](#local-development-setup)
- [Environment Variables](#environment-variables)
- [Running Devora](#running-devora)
- [Development Roadmap](#development-roadmap)
- [Future Improvements](#future-improvements)
- [Deployment](#deployment)
- [Security Principles](#security-principles)
- [Development Philosophy](#development-philosophy)
- [Project Status](#project-status)
- [Vision](#vision)
- [License](#license)
---

# Overview

Most developers practice DSA across multiple platforms.

For example:

* LeetCode for interview preparation
* Codeforces for competitive programming
* GeeksforGeeks for topic-based practice

The problem is that progress is fragmented across these platforms.

A developer may know:

```text
LeetCode:
450 solved

Codeforces:
120 solved

GeeksforGeeks:
180 solved
```

but still not know:

* Which topics are weak?
* Which topics have not been practiced recently?
* Which problems should be solved next?
* Which previously solved problems need revision?
* How much time should be spent on each topic?
* What should today's study plan look like?
* Is the user's performance actually improving?

Devora solves this by creating a centralized DSA intelligence layer.

---

# Why Devora

Devora follows the loop:

```text
Solve
  ↓
Track
  ↓
Analyze
  ↓
Identify Weaknesses
  ↓
Recommend
  ↓
Revise
  ↓
Schedule
  ↓
Improve
```

Instead of simply showing how many problems a user has solved, Devora tries to understand the user's learning behavior.

For example:

```text
Dynamic Programming

Problems Attempted: 32
Problems Solved: 18
Success Rate: 56%

Last Practiced: 8 days ago

Status: Weak

Devora Recommendation:
Practice 2 Medium DP problems today.
```

---

# Core Features

## 1. Landing Page

The public landing page introduces Devora and explains the product.

```text
Devora

Your DSA journey,
intelligently managed.

Track. Analyze. Improve.

[ Get Started ]
[ Login ]
```

---

## 2. User Authentication

Devora supports:

* Email and password signup
* Email and password login
* Google OAuth login
* Forgot password
* Email OTP verification
* Password reset
* JWT-based authentication
* Protected routes

Authentication flow:

```text
User
 ↓
Landing Page
 ↓
Login / Signup
 ↓
Authentication
 ↓
Dashboard
```

Forgot password flow:

```text
Forgot Password
 ↓
Enter Email
 ↓
Generate OTP
 ↓
Send OTP through Email
 ↓
Verify OTP
 ↓
Create New Password
 ↓
Login
```

---

## 3. DSA Progress Tracking

Devora tracks:

* Total problems solved
* Problems attempted
* Accepted submissions
* Failed submissions
* Difficulty distribution
* Platform-wise progress
* Topic-wise progress
* Success rate
* Daily activity
* Weekly activity
* Monthly activity
* Streak
* Revision history

---

## 4. Multi-Platform Support

Devora is designed to support:

### LeetCode

Tracks:

* Problem
* Difficulty
* Submission status
* Language
* Runtime
* Memory
* Submission time

### Codeforces

Tracks:

* Problem
* Rating
* Tags
* Verdict
* Submission
* Contest information

### GeeksforGeeks

Tracks:

* Problem
* Difficulty
* Topic
* Submission status
* Activity

---

## 5. Personalized Recommendations

Devora analyzes user performance and recommends problems based on:

* Weak topics
* Difficulty
* Recent activity
* Historical performance
* Attempt count
* Success rate
* Revision requirements
* User goals

Example:

```text
Recommended Problem

House Robber II
Dynamic Programming
Medium

Why Devora recommends this:

✓ DP is one of your weakest topics
✓ You have not practiced DP recently
✓ You perform well on Medium problems
✓ This problem matches your current level
```

---

## 6. Revision System

Devora tracks problems that need revision.

Initial revision intervals:

```text
1 day
3 days
7 days
14 days
30 days
60 days
```

The intervals can later become adaptive.

For example:

```text
Solved easily
    ↓
Confidence increases
    ↓
Longer revision interval
```

If the user struggles:

```text
Failed revision
    ↓
Confidence decreases
    ↓
Shorter revision interval
```

---

## 7. Personalized Study Plans

Users can specify available study time.

Example:

```text
Available Time: 2 hours
```

Devora might generate:

```text
20 min
Revision

40 min
Dynamic Programming

40 min
Graphs

20 min
Review
```

The recommendation engine determines:

> What should I study?

The scheduler determines:

> When should I study it?

---

## 8. AI DSA Assistant

The long-term goal is to allow users to ask questions such as:

```text
What should I study today?

Which topics am I weak at?

Show my recent progress.

What should I revise today?

Give me a 2-hour study plan.

Why are you recommending this problem?

How am I performing compared to last month?
```

The LLM will access Devora capabilities through MCP.

---

# System Architecture

```text
                         DEVORA
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ↓                 ↓                 ↓
      Web App          Chrome Extension    MCP Server
   React + Vite              │                 │
          │                  │                 ↓
          │           LeetCode/CF/GFG        LLM
          │                  │                 │
          └──────────┬───────┘                 │
                     ↓                         │
                  FastAPI ◄────────────────────┘
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
     PostgreSQL              Redis
                            (later)
          │
          ↓
   ┌───────────────────────┐
   │     Devora Engine     │
   │                       │
   │ Progress              │
   │ Recommendations       │
   │ Revision              │
   │ Scheduling             │
   └───────────────────────┘
```

---

# Technology Stack

## Frontend

* React
* Vite
* TypeScript
* React Router
* Axios
* Tailwind CSS
* Recharts

## Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* Alembic

## Database

* PostgreSQL

## Authentication

* JWT
* Google OAuth
* Password hashing
* Email OTP

## Browser Extension

* TypeScript
* Chrome Manifest V3

## AI

* MCP
* LLM

## Infrastructure

* Docker
* Redis
* Background workers

## Deployment

Planned:

* Vercel
* Railway
* PostgreSQL
* Redis

---

# Project Structure

```text
devora/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── oauth.py
│   │   │
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   └── database.py
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── platform.py
│   │   │   ├── platform_account.py
│   │   │   ├── problem.py
│   │   │   ├── topic.py
│   │   │   ├── problem_topic.py
│   │   │   ├── submission.py
│   │   │   ├── user_problem_stats.py
│   │   │   ├── user_topic_stats.py
│   │   │   ├── daily_activity.py
│   │   │   ├── password_reset.py
│   │   │   ├── study_plan.py
│   │   │   └── study_plan_item.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   │   ├── problem.py
│   │   │   ├── submission.py
│   │   │   ├── progress.py
│   │   │   └── study_plan.py
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── problems.py
│   │   │   ├── submissions.py
│   │   │   ├── progress.py
│   │   │   ├── recommendations.py
│   │   │   └── study_plan.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── email_service.py
│   │   │   ├── submission_service.py
│   │   │   ├── progress_service.py
│   │   │   ├── recommendation_service.py
│   │   │   ├── revision_service.py
│   │   │   └── scheduler_service.py
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── helpers.py
│   │
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   └── script.py.mako
│   │
│   ├── requirements.txt
│   ├── .env
│   └── .gitignore
│
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   ├── landing/
│   │   │   ├── auth/
│   │   │   ├── dashboard/
│   │   │   ├── problems/
│   │   │   ├── topics/
│   │   │   ├── recommendations/
│   │   │   └── study-plan/
│   │   │
│   │   ├── pages/
│   │   │   ├── Landing.tsx
│   │   │   ├── Login.tsx
│   │   │   ├── Signup.tsx
│   │   │   ├── ForgotPassword.tsx
│   │   │   ├── VerifyOTP.tsx
│   │   │   ├── ResetPassword.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Problems.tsx
│   │   │   ├── Topics.tsx
│   │   │   ├── Activity.tsx
│   │   │   ├── Recommendations.tsx
│   │   │   ├── StudyPlan.tsx
│   │   │   └── Settings.tsx
│   │   │
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   └── auth.ts
│   │   │
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   └── useApi.ts
│   │   │
│   │   ├── context/
│   │   │   └── AuthContext.tsx
│   │   │
│   │   ├── types/
│   │   │   ├── auth.ts
│   │   │   ├── problem.ts
│   │   │   ├── progress.ts
│   │   │   └── study-plan.ts
│   │   │
│   │   ├── utils/
│   │   │   └── helpers.ts
│   │   │
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   │
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
│
├── extension/
│   ├── src/
│   │   ├── background/
│   │   │   └── service-worker.ts
│   │   │
│   │   ├── content/
│   │   │   ├── leetcode.ts
│   │   │   ├── codeforces.ts
│   │   │   └── gfg.ts
│   │   │
│   │   ├── popup/
│   │   │   ├── popup.tsx
│   │   │   ├── popup.css
│   │   │   └── components/
│   │   │
│   │   ├── auth/
│   │   │   └── auth.ts
│   │   │
│   │   ├── api/
│   │   │   └── client.ts
│   │   │
│   │   ├── storage/
│   │   │   └── storage.ts
│   │   │
│   │   └── utils/
│   │       └── helpers.ts
│   │
│   ├── public/
│   │   └── icons/
│   │
│   ├── manifest.json
│   ├── package.json
│   └── tsconfig.json
│
│
├── mcp-server/
│   ├── server.py
│   │
│   ├── tools/
│   │   ├── progress.py
│   │   ├── problems.py
│   │   ├── recommendations.py
│   │   ├── revision.py
│   │   └── scheduler.py
│   │
│   ├── schemas/
│   │   └── responses.py
│   │
│   ├── services/
│   │   └── devora_client.py
│   │
│   ├── requirements.txt
│   └── .env
│
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

# Application Flow

## Normal Web Application

```text
User
 ↓
Landing Page
 ↓
Login / Signup
 ↓
Authentication
 ↓
Dashboard
 ↓
Progress / Problems / Topics / Recommendations
 ↓
Study Plan
```

---

# Authentication

Devora uses a centralized authentication system.

## Email Signup

```text
Signup
 ↓
Name + Email + Password
 ↓
FastAPI
 ↓
Validate Input
 ↓
Hash Password
 ↓
Create User
 ↓
Generate JWT
 ↓
Authenticated
```

## Email Login

```text
Login
 ↓
Email + Password
 ↓
FastAPI
 ↓
Find User
 ↓
Verify Password
 ↓
Generate JWT
 ↓
Dashboard
```

## Google Login

```text
Continue with Google
 ↓
Google OAuth
 ↓
Google Authentication
 ↓
Google Callback
 ↓
Find or Create User
 ↓
Generate Devora Authentication
 ↓
Dashboard
```

## Forgot Password

```text
Forgot Password
 ↓
Enter Email
 ↓
Generate 6-digit OTP
 ↓
Store hashed OTP
 ↓
Send Email
 ↓
User enters OTP
 ↓
Verify OTP
 ↓
Create new password
 ↓
Password updated
```

OTP should have a short expiry and limited verification attempts.

---

# DSA Tracking

The Chrome extension acts as the data collection layer.

```text
User solves problem
 ↓
Coding platform
 ↓
Chrome Extension
 ↓
Detect submission
 ↓
Detect verdict
 ↓
POST /api/submissions
 ↓
FastAPI
 ↓
PostgreSQL
 ↓
Progress Engine
```

The extension should track both successful and unsuccessful attempts.

Example:

```text
Problem: House Robber II

Attempts:
1. Wrong Answer
2. Time Limit Exceeded
3. Accepted

Total Attempts: 3
Accepted: 1
Failed: 2
```

---

# Progress Engine

The Progress Engine calculates meaningful statistics from raw submissions.

Metrics include:

```text
Total Problems
Total Solved
Total Attempts
Success Rate
Daily Activity
Weekly Activity
Monthly Activity
Current Streak
Longest Streak
Difficulty Distribution
Platform Distribution
Topic Distribution
```

Example:

```text
Arrays
Solved: 72
Attempted: 90
Success Rate: 80%

Dynamic Programming
Solved: 18
Attempted: 43
Success Rate: 42%

Graphs
Solved: 20
Attempted: 39
Success Rate: 51%
```

---

# Recommendation Engine

The Recommendation Engine determines which problems should be practiced next.

Initial recommendation score:

```text
Recommendation Score =
    Topic Weakness
  + Difficulty Fit
  + Recency
  + Problem Priority
  + Historical Performance
  + Goal Relevance
```

The initial recommendation system is deterministic and score-based.

The LLM is not responsible for inventing recommendations.

The engine produces structured recommendations and the LLM can later explain them naturally.

---

# Revision Engine

The Revision Engine identifies problems that should be revisited.

Initial intervals:

```text
1 day
3 days
7 days
14 days
30 days
60 days
```

The system can later adapt these intervals according to user performance.

Example:

```text
Problem solved easily
 ↓
High confidence
 ↓
Longer revision interval
```

```text
Problem failed during revision
 ↓
Lower confidence
 ↓
Shorter revision interval
```

---

# Study Scheduler

The scheduler determines when the recommended work should be performed.

Input:

```text
Available Time
User Goal
Weak Topics
Revision Due
Difficulty Preference
Platform Preference
Contest Schedule
```

Example:

```text
Available Time: 120 minutes

20 min
Revision

40 min
Dynamic Programming

40 min
Graphs

20 min
Review
```

The distinction is:

```text
Recommendation Engine
        ↓
"What should I study?"

Study Scheduler
        ↓
"When should I study?"
```

---

# Chrome Extension

The Chrome extension is built using Manifest V3.

It acts as Devora's automatic activity collector.

## Extension Flow

```text
LeetCode / Codeforces / GFG
          ↓
Content Script
          ↓
Detect Submission
          ↓
Detect Verdict
          ↓
Background Service Worker
          ↓
Devora API
          ↓
PostgreSQL
```

The extension should not directly access PostgreSQL.

It communicates only with the FastAPI backend.

---

# Extension Authentication

The extension does not have a completely separate Devora account.

Instead:

```text
Extension
 ↓
Connect to Devora
 ↓
Devora Web Authentication
 ↓
Authorize Extension
 ↓
Extension receives secure authorization
 ↓
Extension connected to user's account
```

The same Devora account is used by:

```text
Web Dashboard
+
Chrome Extension
```

---

# MCP Server

MCP provides an interface between the Devora system and an LLM.

Architecture:

```text
User
 ↓
LLM
 ↓
MCP Server
 ↓
Devora Backend
 ↓
PostgreSQL
```

The MCP server should not duplicate Devora business logic.

It should call existing backend services and APIs.

---

# MCP Tools

Planned tools include:

```text
get_progress()
get_topic_progress()
get_recent_activity()
get_weak_topics()
get_problem_stats()
recommend_problems()
recommend_revision()
create_study_plan()
create_daily_timetable()
get_today_plan()
mark_problem_solved()
get_streak()
get_statistics()
sync_platform()
```

Example:

```text
User:

"I have two hours today.
What should I study?"
```

Flow:

```text
User
 ↓
LLM
 ↓
MCP
 ↓
get_progress()
 ↓
get_weak_topics()
 ↓
get_recent_activity()
 ↓
recommend_problems()
 ↓
create_study_plan()
 ↓
LLM
 ↓
Personalized Response
```

---

# Database Design

Devora uses PostgreSQL as the primary database.

## Users

```text
users
----------------
id
name
email
password_hash
google_id
auth_provider
created_at
```

---

## Platforms

```text
platforms
----------------
id
name
```

Example:

```text
1 → LeetCode
2 → Codeforces
3 → GeeksforGeeks
```

---

## Platform Accounts

```text
platform_accounts
-------------------------
id
user_id
platform_id
username
profile_url
last_synced_at
created_at
```

---

## Problems

```text
problems
-------------------------
id
platform_id
external_id
title
url
difficulty
rating
```

---

## Topics

```text
topics
----------------
id
name
```

Examples:

```text
Arrays
Strings
Binary Search
Linked List
Trees
Graphs
Dynamic Programming
Greedy
Backtracking
```

---

## Problem Topics

```text
problem_topics
----------------
id
problem_id
topic_id
```

A problem can belong to multiple topics.

---

## Submissions

```text
submissions
-------------------------
id
user_id
problem_id
status
language
runtime
memory
submitted_at
source
```

---

## User Problem Statistics

```text
user_problem_stats
-------------------------
id
user_id
problem_id
attempt_count
accepted_count
first_attempt_at
last_attempt_at
last_accepted_at
total_time_spent
confidence_score
next_revision_at
```

---

## User Topic Statistics

```text
user_topic_stats
-------------------------
id
user_id
topic_id
attempted
solved
success_rate
average_attempts
average_time
last_practiced_at
confidence_score
```

---

## Daily Activity

```text
daily_activity
-------------------------
id
user_id
date
problems_attempted
problems_solved
minutes_spent
```

---

## Password Reset

```text
password_reset_tokens
-------------------------
id
user_id
otp_hash
expires_at
attempts
used
created_at
```

---

## Study Plans

```text
study_plans
----------------
id
user_id
date
total_minutes
status
created_at
```

---

## Study Plan Items

```text
study_plan_items
-------------------------
id
study_plan_id
problem_id
type
duration
priority
completed
```

Possible types:

```text
NEW_PROBLEM
REVISION
CONTEST
PRACTICE
REVIEW
```

---

# API Structure

Base URL during development:

```text
http://localhost:8000
```

## Authentication

```text
POST /api/auth/signup
POST /api/auth/login

GET  /api/auth/google
GET  /api/auth/google/callback

POST /api/auth/forgot-password
POST /api/auth/verify-otp
POST /api/auth/reset-password

GET /api/auth/me
```

## Users

```text
POST /api/users
GET /api/users/me
```

## Problems

```text
POST /api/problems
GET /api/problems
GET /api/problems/{id}
```

## Submissions

```text
POST /api/submissions
GET /api/submissions
```

## Progress

```text
GET /api/progress
GET /api/progress/daily
GET /api/progress/weekly
GET /api/progress/monthly
```

## Topics

```text
GET /api/topics
GET /api/topics/{id}
```

## Recommendations

```text
GET /api/recommendations
GET /api/recommendations/revision
```

## Study Plans

```text
POST /api/study-plan
GET /api/study-plan/today
GET /api/study-plan/{date}
```

---

# Local Development Setup

## Prerequisites

Install:

* Git
* Python 3.11+
* Node.js
* npm
* PostgreSQL

Optional:

* Docker
* Docker Compose

---

# PostgreSQL Setup

Create the database:

```sql
CREATE DATABASE devora;
```

Default development configuration:

```text
Database: devora
Username: postgres
Host: localhost
Port: 5432
```

---

# Backend Setup

Move into the backend:

```bash
cd backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate on Git Bash:

```bash
source venv/Scripts/activate
```

Activate on Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Backend Environment Variables

Create:

```text
backend/.env
```

Example:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/devora
```

If your PostgreSQL password contains special URL characters, they should be URL encoded.

For example:

```text
@
```

becomes:

```text
%40
```

Never commit `.env` to Git.

---

# Run FastAPI

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

Backend:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

Health check:

```text
http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

---

# Frontend Setup

Move into frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Install required packages:

```bash
npm install react-router-dom axios
```

Run the development server:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

# Frontend ↔ Backend Connection

The frontend communicates with FastAPI through Axios.

Example:

```typescript
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

export default api;
```

Example health request:

```typescript
api.get("/health");
```

Expected response:

```json
{
  "status": "healthy"
}
```

---

# CORS

During local development, FastAPI allows requests from the Vite development server.

Example:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Production origins should be configured separately.

---

# Running Devora

You will typically need at least two terminals.

## Terminal 1

```bash
cd devora/backend
source venv/Scripts/activate
uvicorn app.main:app --reload
```

## Terminal 2

```bash
cd devora/frontend
npm run dev
```

The application will then be available at:

```text
Frontend:
http://localhost:5173

Backend:
http://localhost:8000

API Docs:
http://localhost:8000/docs
```

---

# Development Roadmap

## Phase 1: Foundation

* [x] Create Git repository
* [x] Create project structure
* [x] Setup PostgreSQL
* [x] Setup FastAPI
* [x] Setup React + Vite + TypeScript
* [x] Connect frontend and backend

---

## Phase 2: Authentication

* [x] User database model
* [x] Signup API
* [ ] Login API
* [ ] Password hashing
* [ ] JWT authentication
* [ ] Google OAuth
* [ ] Forgot password
* [ ] Email OTP
* [ ] OTP verification
* [ ] Password reset
* [ ] Protected routes
* [ ] Authentication context

---

## Phase 3: DSA Data Layer

* [ ] Platform model
* [ ] Platform account model
* [ ] Problem model
* [ ] Topic model
* [ ] Problem-topic relationship
* [ ] Submission model
* [ ] User problem statistics
* [ ] User topic statistics
* [ ] Daily activity

---

## Phase 4: Submission API

* [ ] Submission endpoint
* [ ] Duplicate submission handling
* [ ] Submission validation
* [ ] Statistics updates
* [ ] Progress calculations

---

## Phase 5: Chrome Extension

### LeetCode

* [ ] Manifest V3 setup
* [ ] Extension popup
* [ ] Devora authentication
* [ ] Detect current problem
* [ ] Detect submission
* [ ] Detect verdict
* [ ] Send submission to backend
* [ ] Verify synchronization

### Codeforces

* [ ] Codeforces content script
* [ ] Submission detection
* [ ] Verdict detection
* [ ] Backend synchronization

### GeeksforGeeks

* [ ] GFG content script
* [ ] Submission detection
* [ ] Backend synchronization

---

## Phase 6: Dashboard

* [ ] Dashboard layout
* [ ] Total solved
* [ ] Platform statistics
* [ ] Topic statistics
* [ ] Difficulty distribution
* [ ] Daily activity chart
* [ ] Weekly activity
* [ ] Monthly activity
* [ ] Streak
* [ ] Recent submissions

---

## Phase 7: Recommendation Engine

* [ ] Weak topic detection
* [ ] Difficulty matching
* [ ] Recency scoring
* [ ] Historical performance scoring
* [ ] Problem ranking
* [ ] Recommendation explanations

---

## Phase 8: Revision Engine

* [ ] Revision intervals
* [ ] Revision queue
* [ ] Confidence score
* [ ] Adaptive revision
* [ ] Due revision dashboard

---

## Phase 9: Study Scheduler

* [ ] Available-time input
* [ ] Goal selection
* [ ] Daily timetable
* [ ] Revision allocation
* [ ] New problem allocation
* [ ] Topic balancing
* [ ] Study plan tracking

---

## Phase 10: MCP

* [ ] MCP server
* [ ] Progress tools
* [ ] Recommendation tools
* [ ] Revision tools
* [ ] Scheduler tools
* [ ] Problem tools
* [ ] Backend integration

---

## Phase 11: AI Assistant

* [ ] LLM integration
* [ ] MCP tool calling
* [ ] Natural-language progress analysis
* [ ] Personalized recommendations
* [ ] Study-plan generation
* [ ] DSA conversational assistant

---

## Phase 12: Infrastructure

* [ ] Docker
* [ ] Docker Compose
* [ ] Redis
* [ ] Background workers
* [ ] Task queues
* [ ] Caching
* [ ] Rate limiting
* [ ] Logging
* [ ] Monitoring

---

# Future Improvements

Possible future features include:

## Advanced Analytics

* Problem difficulty progression
* Topic mastery score
* Time-to-solve analysis
* Failure pattern analysis
* Contest performance
* Language-wise performance

## Intelligent Recommendations

* Personalized difficulty prediction
* Adaptive problem sequencing
* Learning-path generation
* Similar-problem recommendations
* Pattern-based recommendations

## AI Features

* AI study coach
* Natural-language analytics
* Personalized explanations
* Interview preparation mode
* Contest preparation mode
* Mock interview planning

## Additional Integrations

* GitHub
* CodeChef
* AtCoder
* HackerRank

---

# Redis

Redis will not be required for the initial version.

It can later be introduced for:

```text
Caching
Rate Limiting
Background Jobs
Task Queues
Temporary OTP Data
Session Management
```

Initial architecture:

```text
FastAPI
 ↓
PostgreSQL
```

Later:

```text
FastAPI
 ↓
Redis
 ↓
Background Workers
 ↓
PostgreSQL
```

Redis should only be introduced when there is a concrete requirement for it.

---

# Deployment

Planned production architecture:

```text
                       INTERNET
                           │
              ┌────────────┴────────────┐
              ↓                         ↓
           Vercel                 Chrome Extension
              │
         React + Vite
              │
              ↓
           Railway
           FastAPI
              │
       ┌──────┼──────┐
       ↓      ↓      ↓
 PostgreSQL Redis  Workers
       │
       ↓
 Devora Services
       │
       ├── Progress Engine
       ├── Recommendation Engine
       ├── Revision Engine
       └── Study Scheduler
              │
              ↓
          MCP Server
              │
              ↓
             LLM
```

---

# Security Principles

Devora should follow these principles:

* Passwords must never be stored in plain text.
* Passwords must be securely hashed.
* JWT secrets must be stored in environment variables.
* OAuth credentials must never be committed to Git.
* Email credentials must never be committed to Git.
* `.env` must not be committed.
* OTPs should be stored as hashes.
* OTPs should expire.
* OTP attempts should be limited.
* APIs should validate authentication.
* Users should only access their own data.
* The Chrome extension should never directly access PostgreSQL.
* Production secrets should be stored through the deployment platform's secret management.

---

# Environment Variables

Example root configuration:

```env
DATABASE_URL=
JWT_SECRET=
JWT_ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=

SMTP_HOST=
SMTP_PORT=
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=

FRONTEND_URL=
BACKEND_URL=
```

Never commit real credentials.

Use:

```text
.env
```

for local development and:

```text
.env.example
```

for documenting required variables.

---

# Development Philosophy

Devora follows a layered architecture.

```text
Frontend
   ↓
API
   ↓
Service Layer
   ↓
Database
```

The recommendation system should remain separate from the LLM.

```text
Raw Data
   ↓
Progress Engine
   ↓
Recommendation Engine
   ↓
Study Scheduler
   ↓
MCP
   ↓
LLM
```

The LLM should explain and orchestrate Devora's capabilities rather than becoming the source of truth for user statistics.

---

# Project Status

Devora is currently under active development.

### Current status

```text
Phase 1: Foundation
████████████████████ 100%

Phase 2: Authentication
░░░░░░░░░░░░░░░░░░░░   0%

Phase 3: DSA Tracking
░░░░░░░░░░░░░░░░░░░░   0%

Phase 4: Chrome Extension
░░░░░░░░░░░░░░░░░░░░   0%

Phase 5: Intelligence
░░░░░░░░░░░░░░░░░░░░   0%

Phase 6: MCP + AI
░░░░░░░░░░░░░░░░░░░░   0%
```

---

# Vision

Devora aims to become a personal DSA intelligence platform.

Instead of asking:

> "How many problems have I solved?"

Devora should help answer:

> "What should I solve next, why should I solve it, when should I revise it, and how should I structure my preparation to improve?"

The ultimate goal is:

```text
Track
  ↓
Understand
  ↓
Recommend
  ↓
Schedule
  ↓
Practice
  ↓
Revise
  ↓
Improve
```

---

# License

This project is currently being developed as a personal project.

License information will be added as the project evolves.
