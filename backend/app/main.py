from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router

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


app.include_router(auth_router)
app.include_router(users_router)


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