from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.ai.agent import DevoraAgent
from app.ai.schemas import ChatRequest, ChatResponse
from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.modules.users.models import User

router = APIRouter(
    prefix="/api/ai",
    tags=["AI"],
)


@router.post("/chat", response_model=ChatResponse)
def chat(
    data: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    agent = DevoraAgent(
        user_id=current_user.id,
        db=db,
    )
    response = agent.chat(
        data.message,
    )
    return {
        "response": response,
    }
