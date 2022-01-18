import signal
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Optional, Iterable

from blacktape.lib import match_entities_in_text, match_pattern_in_text


class Pipeline:
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

    def submit_ner_job(self, text: str, entity_types: Optional[Iterable[str]] = None):
        self.futures.append(self.executor.submit(match_entities_in_text, text, self.spacy_model, entity_types))

    def submit_regex_job(self, text: str, pattern: str):
        self.futures.append(self.executor.submit(match_pattern_in_text, text, pattern))


def worker_init():
    """
    Initializer for worker processes that makes them ignore interrupt signals
    https://docs.python.org/3/library/signal.html#signal.signal
    https://docs.python.org/3/library/signal.html#signal.SIG_IGN
    """

    signal.signal(signal.SIGINT, signal.SIG_IGN)
