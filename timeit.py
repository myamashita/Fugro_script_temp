import time

def time_it(func):
    def wrapper(*args, **kargs):
        start_time = time.time()
        result = func(*args, **kargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time} seconds to run.")
        return result
    return wrapper

@time_it
def my_function():
    time.sleep(3)

my_function()
