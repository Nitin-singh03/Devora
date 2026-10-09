from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.dsa.problems.router import router as problems_router
from app.modules.dsa.submissions.router import (
    router as submissions_router
)
from app.modules.dsa.progress.router import router as progress_router
from app.modules.dsa.topics.router import router as topics_router
from app.modules.dsa.recommendations.router import (
    router as recommendations_router
)
from app.modules.dsa.revisions.router import router as revision_router

app = FastAPI(
    title="Devora API",
    description="Extensible Personal Intelligence Platform API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(problems_router)
app.include_router(submissions_router)
app.include_router(progress_router)
app.include_router(topics_router)
app.include_router(recommendations_router)
app.include_router(revision_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to Devora API - Extensible Personal Intelligence Platform"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }