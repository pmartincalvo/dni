class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs
            )
        return cls._instances[cls]


class LastCatchedException(metaclass=Singleton):
    def __init__(self):
        self._last_exception = None

    def store_exception(self, exception):
        self._last_exception = exception

    @property
    def last_exception(self):
        if not self._last_exception:
            raise ValueError("No exception stored.")

        return self._last_exception


def store_exception(exception):
    LastCatchedException().store_exception(exception)


def get_last_catched_exception():
    return LastCatchedException().last_exception
