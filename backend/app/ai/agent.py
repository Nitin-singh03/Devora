import logging
from typing import Any, Dict, Optional
from sqlalchemy.orm import Session
from google.genai import types

from app.ai.client import LLMClient
from app.ai.tools import DEVORA_TOOLS
from app.ai.prompts import SYSTEM_PROMPT
from app.modules.dsa.progress.service import (
    get_overall_progress,
    get_topic_progress,
    get_weak_topics,
)
from app.modules.dsa.revisions.service import get_due_revisions
from app.modules.dsa.recommendations.service import get_recommendations
from app.modules.dsa.planner.service import create_study_plan

logger = logging.getLogger(__name__)


class DevoraAgent:
    def __init__(self, user_id: int, db: Session):
        self.user_id = user_id
        self.db = db
        self.llm = LLMClient()

    def execute_tool(self, name: str, arguments: Optional[Dict[str, Any]] = None) -> Any:
        arguments = arguments or {}

        if name == "get_progress":
            return get_overall_progress(self.user_id, self.db)

        elif name == "get_topic_progress":
            return get_topic_progress(self.user_id, self.db)

        elif name == "get_weak_topics":
            return get_weak_topics(self.user_id, self.db)

        elif name == "recommend_problems":
            limit = arguments.get("limit", 5)
            return get_recommendations(self.user_id, self.db, limit=limit)

        elif name == "get_due_revisions":
            revisions = get_due_revisions(self.user_id, self.db)
            return [
                {
                    "problem_id": r.problem_id,
                    "revision_count": r.revision_count,
                    "confidence": r.confidence,
                    "next_revision_at": (
                        r.next_revision_at.isoformat()
                        if r.next_revision_at
                        else None
                    ),
                }
                for r in revisions
            ]

        elif name == "get_today_plan":
            return create_study_plan(self.user_id, self.db)

        raise ValueError(f"Unknown tool: {name}")

    def chat(self, user_message: str) -> str:
        """
        Runs the agentic loop:
        1. Formulates the prompt with system instructions and user message.
        2. Generates a decision with available Devora tools.
        3. If the LLM requests a tool call, executes the tool via Devora services.
        4. Sends the tool execution result back to the LLM to explain and answer.
        5. Returns the final response.
        """
        user_content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=f"{SYSTEM_PROMPT}\n\nUser: {user_message}")]
        )

        response = self.llm.generate(
            contents=[user_content],
            tools=DEVORA_TOOLS,
        )

        if not response.function_calls:
            return response.text or ""

        # Handle tool call(s)
        model_turn_content = response.candidates[0].content
        tool_parts = []

        for call in response.function_calls:
            try:
                result = self.execute_tool(call.name, call.args)
                tool_parts.append(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": result},
                    )
                )
            except Exception as e:
                logger.error(f"Error executing tool {call.name}: {e}")
                tool_parts.append(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"error": str(e)},
                    )
                )

        tool_response_content = types.Content(
            role="user",
            parts=tool_parts,
        )

        final_response = self.llm.generate(
            contents=[user_content, model_turn_content, tool_response_content],
            tools=DEVORA_TOOLS,
        )

        return final_response.text or ""
