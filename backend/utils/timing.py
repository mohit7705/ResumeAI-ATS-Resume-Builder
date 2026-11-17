import logging
import time
from contextlib import contextmanager


log = logging.getLogger("resumeai.timing")


@contextmanager
def timed(name: str):
    """Log the duration of a pipeline step."""
    start = time.perf_counter()
    try:
        yield
    finally:
        log.info("%-14s %.2fs", name, time.perf_counter() - start)
