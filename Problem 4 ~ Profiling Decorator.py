from time import sleep
from datetime import datetime


def profile(func):
    def wrapper(*args):
        start = datetime.now()
        res = func(*args)
        duration = datetime.now() - start
        with open("performance.log", "a") as f:
            text = "{} - {}({}) - {} \n".format(start, func.__name__, *args, duration)
            f.write(text)
            f.close()
        return res
    return wrapper


@profile
def foo(x):
    sleep(2)
    return x ** 2


foo(4)
foo(5)
foo(26)
