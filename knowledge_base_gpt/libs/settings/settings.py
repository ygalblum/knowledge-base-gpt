# pylint:disable=R0903
""" Settings for the application """
from typing import Literal

from pydantic import BaseModel, Field

from knowledge_base_gpt.libs.settings.settings_loader import load_active_settings


class SlackBotSettings(BaseModel):
    """ Slackbot Settings """
    app_token: str = Field(
        description="Slack App Token"
    )
    bot_token: str = Field(
        description="Slack Bot Token"
    )
    forward_channel: str = Field(
        description="Name of the channel to forward unresolved conversations to"
    )
    base_url: str = Field(
        "",
        description="Base URL of the Slack server - used for testing"
    )


class LLMSettings(BaseModel):
    """ LLM Settings """
    mode: Literal["ollama", "vllm", "fake"] = Field(
        'ollama',
        description="LLM Backend to use for chat"
    )
    context_window: int = Field(
        3900,
        description="The maximum number of context tokens for the model.",
    )
    temperature: float = Field(
        0.1,
        description="The temperature of the model. "
        "Increasing the temperature will make the model answer more creatively. "
        "A value of 0.1 would be more factual.",
    )
    verbose: bool = Field(
        False,
        description="Verbosity flag for logging to stdout."
    )
    num_documents: int = Field(
        4,
        description="Amount of documents to retrieve"
    )


class EmbeddingSettings(BaseModel):
    """ Embedding Settings """
    mode: Literal["hugging_face", "ollama", "infinity", "fake"] = Field(
        'hugging_face',
        description="LLM Backend to use for embedding"
    )
    temperature: float = Field(
        0.1,
        description="The temperature of the model. "
        "Increasing the temperature will make the model answer more creatively. "
        "A value of 0.1 would be more factual.",
    )


class GoogleDriveSettings(BaseModel):
    """ Google Drive Settings """
    service_key_file: str = Field(
        None,
        description="Path a the Google Service Key file"
    )
    folder_id: str = Field(
        None,
        description="ID of the Google Drive Folder to ingest"
    )


class OllamaSettings(BaseModel):
    """ Ollama Settings """
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
        description="Tail free sampling is used to reduce the impact of less probable tokens from the output. "
        "A higher value (e.g., 2.0) will reduce the impact more, while a value of 1.0 disables this setting.",
    )
    num_predict: int = Field(
        None,
        description="Maximum number of tokens to predict when generating text. "
        "(Default: 128, -1 = infinite generation, -2 = fill context)",
    )
    top_k: int = Field(
        40,
        description="Reduces the probability of generating nonsense. "
        "A higher value (e.g. 100) will give more diverse answers, "
        "while a lower value (e.g. 10) will be more conservative. (Default: 40)",
    )
    top_p: float = Field(
        0.9,
        description="Works together with top-k. "
        "A higher value (e.g., 0.95) will lead to more diverse text, "
        "while a lower value (e.g., 0.5) will generate more focused and conservative text. (Default: 0.9)",
    )
    repeat_last_n: int = Field(
        64,
        description="Sets how far back for the model to look back to prevent repetition. "
        "(Default: 64, 0 = disabled, -1 = num_ctx)",
    )
    repeat_penalty: float = Field(
        1.1,
        description="Sets how strongly to penalize repetitions. "
        "A higher value (e.g., 1.5) will penalize repetitions more strongly, "
        "while a lower value (e.g., 0.9) will be more lenient. (Default: 1.1)",
    )


class FakeModelSettings(BaseModel):
    """ Settings for fake model - used for testing """
    response_path: str = Field(
        None,
        description="Path to a json file with an array of fake responses"
    )


class VLLMSettings(BaseModel):
    """ vLLM Settings """
    api_base: str = Field(
        "http://localhost:8000/v1",
        description="Base URL of vLLM OpenAI API. Example: 'http://localhost:8000/v1'.",
    )
    llm_model: str = Field(
        None,
        description="Model to use. Example: 'mistralai/Mistral-7B-Instruct-v0.2'.",
    )


class HuggingFaceSettings(BaseModel):
    """ Hugging Face Settings """
    embedding_model: str = Field(
        None,
        description="Model to use. Example: 'nomic-embed-text'.",
    )


class InfinitySettings(BaseModel):
    """ Infinity Settings """
    api_url: str = Field(
        "http://localhost:7997",
        description="Base URL of Infinity API. Example: 'https://localhost:7997'.",
    )
    embedding_model: str = Field(
        None,
        description="Model to use. Example: 'nomic-embed-text'.",
    )


class HistorySettings(BaseModel):
    """ History Settings """
    mode: Literal['memory', 'redis'] = Field(
        'memory',
        description="Mode of History manager"
    )


class RedisSettings(BaseModel):
    """ Redis Settings """
    host: str = Field(
        'localhost',
        description="FQDN for redis"
    )
    username: str = Field(
        '',
        description="Redis username if needed"
    )
    password: str = Field(
        '',
        description="Redis password if needed"
    )
    ttl: int = Field(
        3000,
        description="Time to Live for keys"
    )
    chat_identifier_key_prefix: str = Field(
        "chat:",
        description="Prefix for the chat identifier key"
    )


class LogSettings(BaseModel):
    """ Logging Settings """
    chat_log_enabled: bool = Field(
        True,
        description="Enable/Disable chat logs"
    )

    chat_log_path: str = Field(
        "./chatlog.log",
        description="Path to store the chat logs"
    )

    chat_log_max_bytes: int = Field(
        1024 * 1024,
        description="Maximal size of the chat log file before rotation"
    )

    chat_log_backup_count: int = Field(
        3,
        description="Number of rotated chat log files to keep"
    )

    application_log_level: str = Field(
        "INFO",
        description="Application logs debug level"
    )

    application_log_path: str = Field(
        "",
        description="Path to store the application logs. When not set, log to stdout"
    )

    application_log_max_bytes: int = Field(
        1024 * 1024,
        description=(
            "Maximal size of the application log file before rotation. "
            "Relevant only if application_log_path is set."
        )
    )

    application_log_backup_count: int = Field(
        3,
        description=(
            "Number of rotated application log files to keep. "
            "Relevant only if application_log_path is set."
        )
    )


class ContentLoaderSettings(BaseModel):
    """ Content Loader Settings """
    mode: Literal['google_drive', 'mock'] = Field(
        'google_drive',
        description="Type of Content Loader to use"
    )


class TextSpliterSettings(BaseModel):
    """ Text Splitter Settings """
    chunk_size: int = Field(
        500,
        description="Size of each chunk"
    )
    chunk_overlap: int = Field(
        50,
        description="Overlap between chunks"
    )


class VectorStoreSettings(BaseModel):
    """ Vector Store Settings """
    mode: Literal['chroma', 'memory'] = Field(
        'chroma',
        description="Type of vector store"
    )
    persist_directory: str = Field(
        './db',
        description="Path to store the embedding DB"
    )


class Settings(BaseModel):
    """ Application Settings """
    slackbot: SlackBotSettings
    llm: LLMSettings
    ollama: OllamaSettings
    history: HistorySettings
    redis: RedisSettings
    log: LogSettings
    content_loader: ContentLoaderSettings
    google_drive: GoogleDriveSettings
    text_splitter: TextSpliterSettings
    embedding: EmbeddingSettings
    hugging_face: HuggingFaceSettings
    infinity: InfinitySettings
    vectorstore: VectorStoreSettings
    fake_model: FakeModelSettings
    vllm: VLLMSettings


# This is visible just for DI or testing purposes.
# Use dependency injection or `settings()` method instead.
unsafe_settings = load_active_settings()

# This is visible just for DI or testing purposes.
# Use dependency injection or `settings()` method instead.
unsafe_typed_settings = Settings(**unsafe_settings)


def settings() -> Settings:
    """Get the current loaded settings from the DI container.

    This method exists to keep compatibility with the existing code,
    that require global access to the settings.

    For regular components use dependency injection instead.
    """
    from knowledge_base_gpt.libs.injector.di import global_injector  # pylint:disable=C0415

    return global_injector.get(Settings)
