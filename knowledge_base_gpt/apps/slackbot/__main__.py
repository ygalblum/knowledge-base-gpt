from knowledge_base_gpt.libs.injector.di import global_injector
from knowledge_base_gpt.apps.slackbot.slack_bot import KnowledgeBaseSlackBot

global_injector.get(KnowledgeBaseSlackBot).run()
