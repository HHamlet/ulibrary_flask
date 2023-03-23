"""Problem 4 -- Profiling Decorator"""

from time import sleep
from datetime import datetime


def profile(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        res = func(*args, **kwargs)
        duration = datetime.now() - start
        with open("performance.log", "a") as f:
            if kwargs is None:
                text = "{} - {}({}) - {} \n".format(start, func.__name__, *args, duration)
            else:
                text = "{} - {}({}, {}) - {} \n".format(start, func.__name__, *args, **kwargs, duration)
            f.write(text)
        return res
    return wrapper


@profile
def foo(x):
    sleep(2)
    return x ** 2


foo(4)
foo(5)
foo(26)
