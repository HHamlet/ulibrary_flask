from time import sleep
from datetime import datetime


def profile(func):
    def wrapper(*args):
        start = datetime.now()
        res = func(*args)
        duration = datetime.now() - start
        f = open("performance.log", "w")
        print(f"{start} - {func.__name__}{args} - {duration} \n", file=f)
        return res

    return wrapper


@profile
def foo(x):
    sleep(2)
    return x ** 2


foo(4)
