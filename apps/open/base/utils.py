import time


class StopWatch:
    def __init__(self):
        self._start = time.perf_counter()

    def stop(self):
        stopwatch = time.perf_counter() - self._start
        print(f"Request completed in {stopwatch:.0f}ms")
