import threading
import time
from contextlib import contextmanager

class LLMGovernor:
    def __init__(self, max_concurrent: int = 1, delay_seconds: float = 1.0):
        self.semaphore = threading.BoundedSemaphore(max_concurrent)
        self.delay = delay_seconds

    @contextmanager
    def guard(self):
        self.semaphore.acquire()
        try:
            yield
        finally:
            if self.delay > 0:
                time.sleep(self.delay)
                
            self.semaphore.release()