from typing import Literal

from pydantic import BaseModel, Field

from knowledge_base_gpt.libs.settings.settings_loader import load_active_settings


class SlackBotSettings(BaseModel):
    app_token: str = Field(
        description="Slack App Token"
    )
    bot_token: str = Field(
        description="Slack Bot Token"
    )
    forward_channel: str = Field(
        description="Name of the channel to forward unresolved conversations to"
    )


class LLMSettings(BaseModel):
    mode: Literal["ollama", "mock"] = Field(
        'ollama',
        description="LLM Backend to use"
    )
    context_window: int = Field(
        3900,
        description="The maximum number of context tokens for the model.",
    )
    temperature: float = Field(
        0.1,
        description="The temperature of the model. Increasing the temperature will make the model answer more creatively. A value of 0.1 would be more factual.",
    )


class OllamaSettings(BaseModel):
    api_base: str = Field(
        "http://localhost:11434",
        description="Base URL of Ollama API. Example: 'https://localhost:11434'.",
    )
    llm_model: str = Field(
        None,
        description="Model to use. Example: 'llama2-uncensored'.",
    )
    embedding_model: str = Field(
        None,
        description="Model to use. Example: 'nomic-embed-text'.",
    )
    tfs_z: float = Field(
        1.0,
        description="Tail free sampling is used to reduce the impact of less probable tokens from the output. A higher value (e.g., 2.0) will reduce the impact more, while a value of 1.0 disables this setting.",
    )
    num_predict: int = Field(
        None,
        description="Maximum number of tokens to predict when generating text. (Default: 128, -1 = infinite generation, -2 = fill context)",
    )
    top_k: int = Field(
        40,
        description="Reduces the probability of generating nonsense. A higher value (e.g. 100) will give more diverse answers, while a lower value (e.g. 10) will be more conservative. (Default: 40)",
    )
    top_p: float = Field(
        0.9,
        description="Works together with top-k. A higher value (e.g., 0.95) will lead to more diverse text, while a lower value (e.g., 0.5) will generate more focused and conservative text. (Default: 0.9)",
    )
    repeat_last_n: int = Field(
        64,
        description="Sets how far back for the model to look back to prevent repetition. (Default: 64, 0 = disabled, -1 = num_ctx)",
    )
    repeat_penalty: float = Field(
        1.1,
        description="Sets how strongly to penalize repetitions. A higher value (e.g., 1.5) will penalize repetitions more strongly, while a lower value (e.g., 0.9) will be more lenient. (Default: 1.1)",
    )
    verbose: bool = Field(
        False,
        description="Verbosity flag for logging to stdout."
    )


class RedisSettings(BaseModel):
    host: str = Field(
        'localhost',
        description="FQDN for redis"
    )
    password: str = Field(
        None,
        description="Redis password if needed"
    )
    ttl: int = Field(
        3000,
        description="Time to Live for keys"
    )

class Settings(BaseModel):
    slackbot: SlackBotSettings
    llm: LLMSettings
    ollama: OllamaSettings
    redis: RedisSettings


"""
This is visible just for DI or testing purposes.

Use dependency injection or `settings()` method instead.
"""
unsafe_settings = load_active_settings()

"""
This is visible just for DI or testing purposes.

Use dependency injection or `settings()` method instead.
"""
unsafe_typed_settings = Settings(**unsafe_settings)


def settings() -> Settings:
    """Get the current loaded settings from the DI container.

    This method exists to keep compatibility with the existing code,
    that require global access to the settings.

    For regular components use dependency injection instead.
    """
    from knowledge_base_gpt.libs.injector.di import global_injector

    return global_injector.get(Settings)
