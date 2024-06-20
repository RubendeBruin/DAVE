import time

class TimeElapsed:
    def __init__(self):
        self.last_time = time.time()

    def elapsed(self, message):
        current_time = time.time()
        elapsed_time = current_time - self.last_time
        self.last_time = current_time

        if message:
            print(f'{message}: {elapsed_time:.3f} seconds')

        return elapsed_time

if __name__ == '__main__':
    timer = TimeElapsed()
    timer.elapsed('Starting')
    time.sleep(1)
    timer.elapsed('Sleeping')
    import numpy as np
    timer.elapsed('Imporing numpy took')