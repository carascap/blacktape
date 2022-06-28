import hashlib
import signal
from functools import partial
from pathlib import Path

from sqlalchemy.orm.session import Session

import blacktape
from blacktape.models import Configuration


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


def record_workflow_config(session: Session, **kwargs) -> None:
    """
    Store the current workflow run's configuration in the DB
    """

    session.add(Configuration(name="blacktape_version", value=blacktape.__version__))

    session.add_all(
        Configuration(name=key, value=str(value)) for key, value in kwargs.items()
    )

    session.commit()
