from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class LLMClient(ABC):
    """
    Abstract interface for LLM providers (Gemini, OpenAI, Anthropic, Local models).
    Decouples the core Devora reasoning agent from any provider-specific SDK.
    """

    def __init__(self):
        pass

    @abstractmethod
    def generate(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
    ) -> Any:
        """
        Generate a text response or tool call decision from the model.
        """
        raise NotImplementedError
