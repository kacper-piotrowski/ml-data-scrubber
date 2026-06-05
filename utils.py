import time
from datetime import datetime

def time_func(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        with open("log_file.log", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()}: {func.__name__}: {end-start}\n")
        return result
    return wrapper

class BadRowException(Exception):
    def __init__(self, row_num, error_text):
        self.row_num = row_num
        self.error_text = error_text

class NoDatasetException(Exception):
    def __init__(self, error_text):
        self.error_text = error_text

class InvalidBatchNumberException(Exception):
    def __init__(self, error_text):
        self.error_text = error_text