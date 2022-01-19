import signal


def worker_init():
    """
    Initializer for worker processes that makes them ignore interrupt signals
    https://docs.python.org/3/library/signal.html#signal.signal
    https://docs.python.org/3/library/signal.html#signal.SIG_IGN
    """

    signal.signal(signal.SIGINT, signal.SIG_IGN)
