from threading import Thread
import time

a = 0


def function(arg):
    global a
    for _ in range(arg):
        a += 1
        time.sleep(0)


def main():
    threads = []
    x1 = time.time()
    for i in range(5):
        thread = Thread(target=function, args=(1000000,))
        thread.start()
        threads.append(thread)

    [t.join() for t in threads]
    x2 = time.time()
    print("----------------------", a)  # ???
    print("time", x2-x1)  # ???


main()
