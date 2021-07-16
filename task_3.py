
from concurrent.futures import ThreadPoolExecutor
import time

a = 0


def function(arg):
    global a

    for _ in range(arg):
        a += 1
        time.sleep(0)


def main():
    quantity = 5

    with ThreadPoolExecutor(max_workers=quantity) as executor:
        [executor.submit(function, 1000000) for _ in range(quantity)]

    print("----------------------", a)  # !!!


main()
