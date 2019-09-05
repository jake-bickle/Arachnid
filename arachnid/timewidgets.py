import time


class Stopwatch:
    def __init__(self, seconds=0):
        self.time_limit = seconds

    def start(self):
        self.start_time = time.time()

    def restart(self):
        self.start()

    def wait(self):
        elapsed_time = time.time() - self.start_time
        remaining_time = self.time_limit - elapsed_time
        if remaining_time > 0:
            time.sleep(remaining_time)


class Timer:
    def start(self):
        self.start_time = time.time()

    def restart(self):
        self.start()

    def elapsed(self):
        return time.time() - self.start_time
