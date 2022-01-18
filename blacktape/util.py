import logging
import multiprocessing
import signal
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Callable, List

logger = multiprocessing.log_to_stderr(level=logging.INFO)


def worker_init():
    """
    Initializer for worker processes that makes them ignore interrupt signals
    https://docs.python.org/3/library/signal.html#signal.signal
    https://docs.python.org/3/library/signal.html#signal.SIG_IGN
    """

    signal.signal(signal.SIGINT, signal.SIG_IGN)


def process_files(files: List[Path], job: Callable, *args, **kwargs) -> None:
    futures = []

    with ProcessPoolExecutor(initializer=worker_init) as executor:

        # Iterate over files
        for f in files:
            futures.append(executor.submit(job, f, *args, **kwargs))

        # Handle exceptions in worker processes
        for future in as_completed(futures):
            try:
                res = future.result()
                # Make ORM object from res
            except Exception as exc:
                logger.exception(exc)
