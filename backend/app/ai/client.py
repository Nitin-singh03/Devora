from typing import Any, List, Optional
from google import genai
from google.genai import types
from google.genai.errors import APIError
from app.core.config import settings

CANDIDATE_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.8-flash",
    "gemini-3.5-flash",
]


class LLMClient:
    def __init__(self, model: Optional[str] = None):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )
        self.preferred_model = model

    def _prepare_tools(self, tools: Optional[List[Any]]) -> Optional[List[types.Tool]]:
        if not tools:
            return None
        if isinstance(tools, list) and len(tools) > 0 and isinstance(tools[0], types.Tool):
            return tools

        declarations = []
        for t in tools:
            if isinstance(t, types.Tool):
                return tools
            fn = t.get("function", t) if isinstance(t, dict) else t
            if isinstance(fn, dict) and "name" in fn:
                declarations.append(
                    types.FunctionDeclaration(
                        name=fn["name"],
                        description=fn.get("description", ""),
                        parameters_json_schema=fn.get("parameters") or {"type": "object", "properties": {}},
                    )
                )
        if declarations:
            return [types.Tool(function_declarations=declarations)]
        return tools

    def generate(self, contents: Any, tools: Optional[List[Any]] = None):
        config = {}
        prepared_tools = self._prepare_tools(tools)
        if prepared_tools:
            config["tools"] = prepared_tools

        models_to_try = [self.preferred_model] if self.preferred_model else CANDIDATE_MODELS
        last_error = None

        for model_name in models_to_try:
            try:
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=config,
                )
                return response
            except APIError as e:
                last_error = e
                # Fallback on transient 503 (demand spike) or 404 (retired model)
                if getattr(e, "code", None) in (404, 503):
                    continue
                raise
        if last_error:
            raise last_error
