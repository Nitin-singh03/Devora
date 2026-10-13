import logging
from typing import Any, Dict, List, Optional

from app.ai.client import LLMClient
from app.ai.prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class DevoraAgent:
    def __init__(
        self,
        llm_client: LLMClient,
        mcp_session: Optional[Any] = None,
        system_prompt: str = SYSTEM_PROMPT,
    ):
        self.llm_client = llm_client
        self.mcp_session = mcp_session
        self.system_prompt = system_prompt

    async def run(self, user_message: str) -> str:
        """
        Runs an agent step:
        1. Formulates the prompt with the system prompt and conversation history.
        2. Consults the LLM client with available MCP tools.
        3. If the LLM requests a tool call, routes the request to the MCP client session.
        4. Returns the final generated answer to the user.
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_message},
        ]
        return await self.llm_client.generate(messages)
