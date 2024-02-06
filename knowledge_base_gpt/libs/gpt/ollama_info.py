from contextlib import contextmanager
from contextvars import ContextVar
import threading
from typing import Any, Dict, List, Optional, Generator

from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from langchain_core.tracers.context import register_configure_hook


class OllamaMetrics():
    prompt_eval_count: int = 0
    eval_count: int = 0
    load_duration: int = 0
    prompt_eval_duration: int =0
    eval_duration: int = 0
    total_duration: int = 0

    def __repr__(self) -> str:
        return (
            f"Tokens Used: {self.prompt_eval_count + self.eval_count}\n"
            f"\tPrompt Tokens: {self.prompt_eval_count}\n"
            f"\tCompletion Tokens: {self.eval_count}\n"
            f"Total duration: {self.total_duration}\n"
            f"\t Model loading duration: {self.load_duration}\n"
            f"\t Prompt evaluation duration: {self.prompt_eval_duration}\n"
            f"\t Response evaluation duration: {self.eval_duration}"
        )

    def to_json(self) -> dict:
        return {
            "prompt_eval_count": self.prompt_eval_count,
            "eval_count": self.eval_count,
            "load_duration": self.load_duration,
            "prompt_eval_duration": self.prompt_eval_duration,
            "eval_duration": self.eval_duration,
            "total_duration": self.total_duration
        }


class OllamaCallbackHandler(BaseCallbackHandler):
    """Callback Handler that tracks Ollama info."""

    def __init__(self) -> None:
        super().__init__()
        self._lock = threading.Lock()
        self.metrics: List[OllamaMetrics] = []

    def __repr__(self) -> str:
        ret_str = ""
        for i, metric in enumerate(self.metrics):
            ret_str += f"Request #{i+1}:\n" + metric.__repr__() + "\n"
        return ret_str

    @property
    def always_verbose(self) -> bool:
        """Whether to call verbose callbacks even if verbose is False."""
        return True

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Print out the prompts."""
        pass

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Print out the token."""
        pass

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Collect token usage."""
        if len(response.generations) == 0 or len(response.generations[0]) == 0:
            return None

        info = response.generations[0][0].generation_info

        metrics = OllamaMetrics()
        metrics.prompt_eval_count = info.get("prompt_eval_count", 0)
        metrics.eval_count = info.get("eval_count", 0)
        metrics.load_duration = info.get("load_duration", 0)
        metrics.prompt_eval_duration = info.get("prompt_eval_duration", 0)
        metrics.eval_duration = info.get("eval_duration", 0)
        metrics.total_duration = info.get("total_duration", 0)

        # update shared state behind lock
        with self._lock:
            self.metrics.append(metrics)

    def __copy__(self) -> "OllamaCallbackHandler":
        """Return a copy of the callback handler."""
        return self

    def __deepcopy__(self, memo: Any) -> "OllamaCallbackHandler":
        """Return a deep copy of the callback handler."""
        return self


ollama_callback_var: ContextVar[Optional[OllamaCallbackHandler]] = ContextVar(
    "ollama_callback", default=None
)

register_configure_hook(ollama_callback_var, True)

@contextmanager
def get_ollama_callback() -> Generator[OllamaCallbackHandler, None, None]:
    """Get the Ollama callback handler in a context manager.
    which conveniently exposes token information.

    Returns:
        OllamaCallbackHandler: The OpenAI callback handler.

    Example:
        >>> with get_ollama_callback() as cb:
        ...     # Use the Ollama callback handler
    """
    cb = OllamaCallbackHandler()
    ollama_callback_var.set(cb)
    yield cb
    ollama_callback_var.set(None)
