from pydantic import BaseModel, Field

from knowledge_base_gpt.libs.settings.settings_loader import load_active_settings


class SlackBot(BaseModel):
    app_token: str = Field(
        description="Slack App Token"
    )

    bot_token: str = Field(
        description="Slack Bot Token"
    )

    forward_channel: str = Field(
        description="Name of the channel to forward unresolved conversations to"
    )


class Settings(BaseModel):
    slackbot: SlackBot

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
