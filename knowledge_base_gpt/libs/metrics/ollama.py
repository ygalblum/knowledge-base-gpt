import json
from typing import List
import uuid

from knowledge_base_gpt.libs.gpt.ollama_info import OllamaMetrics


class OllamaMetricsExporter():
    def __init__(self, path: str):
        self._path = path

    def save_metrics(self, metrics: List[OllamaMetrics], identifier: str = None):
        answer_index = 0
        log_entries = []

        if len(metrics) > 2:
            return

        if identifier is None:
            identifier = str(uuid.uuid4())

        if len(metrics) == 2:
            log_entries.append(self._create_entry(identifier, "question_generation", metrics[0]))
            answer_index = 1

        log_entries.append(self._create_entry(identifier, "answer_generation", metrics[answer_index]))

        with open(self._path, "a+") as f:
            for log_entry in log_entries:
                f.write(f"{json.dumps(log_entry)}\n")

    @staticmethod
    def _create_entry(identifier: str, stage: str, metric: OllamaMetrics) -> dict:
        entry = metric.to_json()
        entry['identifier'] =  identifier
        entry['stage'] = stage
        return entry
