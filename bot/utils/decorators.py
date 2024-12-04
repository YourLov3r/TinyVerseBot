from functools import wraps
import time


def async_timer_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        end = time.perf_counter()
        execution_time = end - start
        print(
            f"Execution time: {execution_time:.4f} seconds | Function: {func.__name__}"
        )
        return result

    return wrapper


def sync_timer_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        execution_time = end - start
        print(
            f"Execution time: {execution_time:.4f} seconds | Function: {func.__name__}"
        )
        return result

    return wrapper
