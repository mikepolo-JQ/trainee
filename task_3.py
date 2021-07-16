import threading
from concurrent.futures import ThreadPoolExecutor
import time


class Adding:
    def __init__(self):
        self.a = 0
        self._lock = threading.Lock()

    def plus_one(self, arg):
        with self._lock:
            for _ in range(arg):
                self.a += 1


def main():
    quantity = 5
    obj = Adding()
    start = time.time()

    with ThreadPoolExecutor(max_workers=quantity) as executor:
        [executor.submit(obj.plus_one, 1000000) for _ in range(quantity)]

    finish = time.time()

    print(f"Time to complete: {finish - start:.2f}")
    print("----------------------", obj.a)  # !!!


main()
