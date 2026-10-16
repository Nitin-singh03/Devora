from typing import Any, Dict, List
from google.genai import types


DEVORA_TOOLS: List[Dict[str, Any]] = [
    {
        "type": "function",
        "function": {
            "name": "get_progress",
            "description": "Get the user's overall DSA progress including attempted, solved, submissions and success rate.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_topic_progress",
            "description": "Get the user's DSA progress broken down by topic.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weak_topics",
            "description": "Find the user's weak DSA topics based on their performance.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_due_revisions",
            "description": "Get the authenticated user's DSA problems currently due for revision.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "recommend_problems",
            "description": "Get personalized DSA problem recommendations for the authenticated user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of problems to recommend (default 5).",
                    }
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_today_plan",
            "description": "Get the authenticated user's personalized study plan for today.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
]


def get_gemini_tools() -> List[types.Tool]:
    """Convert DEVORA_TOOLS schemas into Gemini SDK types.Tool."""
    declarations = []
    for tool in DEVORA_TOOLS:
        fn = tool.get("function", tool)
        declarations.append(
            types.FunctionDeclaration(
                name=fn["name"],
                description=fn.get("description", ""),
                parameters_json_schema=fn.get("parameters") or {"type": "object", "properties": {}},
            )
        )
    return [types.Tool(function_declarations=declarations)]
