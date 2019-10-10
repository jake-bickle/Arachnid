import time


class Timer:
    def __init__(self, seconds=0):
        self.start_time = None
        self.time_limit = seconds

    def start(self):
        self.start_time = time.time()

    def restart(self):
        self.start()

    def elapsed(self):
        return time.time() - self.start_time

    def wait(self):
        elapsed_time = time.time() - self.start_time
        remaining_time = self.time_limit - elapsed_time
        if remaining_time > 0:
            time.sleep(remaining_time)
