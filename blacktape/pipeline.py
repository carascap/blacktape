from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Iterable, Optional

from blacktape.lib import match_entities_in_text, match_pattern_in_text
from blacktape.util import worker_init


class Pipeline:
    """
    Wrapper around ProcessPoolExecutor
    """

    def __init__(self, spacy_model: Optional[str] = None):
        self.spacy_model = spacy_model
        self.executor = ProcessPoolExecutor(initializer=worker_init)
        self.futures = []

    def results(self):
        for future in as_completed(self.futures):
            yield future.result()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.executor.shutdown()

    def submit_ner_job(
        self, text: str, entity_types: Optional[Iterable[str]] = None, **kwargs
    ):
        self.futures.append(
            self.executor.submit(
                match_entities_in_text, text, self.spacy_model, entity_types, **kwargs
            )
        )

    def submit_regex_job(self, text: str, pattern: str, label: str):
        self.futures.append(
            self.executor.submit(match_pattern_in_text, text, pattern, label)
        )
