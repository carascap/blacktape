import hashlib
import signal
from functools import partial
from pathlib import Path


def worker_init():
    """
    Initializer for worker processes that makes them ignore interrupt signals
    https://docs.python.org/3/library/signal.html#signal.signal
    https://docs.python.org/3/library/signal.html#signal.SIG_IGN
    """

    signal.signal(signal.SIGINT, signal.SIG_IGN)


def md5_file(path: Path) -> str:
    md5 = hashlib.md5()

    with path.open(mode="rb") as f:
        for block in iter(partial(f.read, 128), b""):
            md5.update(block)

    return md5.hexdigest()
