import asyncio
from datetime import datetime
import sys
import os
import inspect
from tg_userbot import client, DEBUG


loop = asyncio.get_event_loop()


def timer(seconds):
    """
    A decorator that runs a decorated function every x seconds.

    Args:

    seconds (int): Updates the function every given second
    """

    def decorator(fcn):
        async def wrapper():

            if seconds == 0:
                return
            while not client.is_connected():
                await asyncio.sleep(1)
            while True:
                await fcn()
                await asyncio.sleep(seconds)
        loop.create_task(wrapper())

        if seconds == 0:
            return

        return fcn
        return wrapper
    return decorator


def log_to_str(v):
    try:
        return str(v).replace("\n", "\\n")
    except Exception:
        return "<ERROR: CANNOT PRINT>"


def log_exception(func):

    async def wrapper(*args, **kwds):
        __lgw_marker_local__ = 0

        try:
            return await func(*args, **kwds)
        except Exception as e:

            exc_time = datetime.now().strftime("%m_%d_%H:%M:%S")

            file_name = f"{exc_time}_{type(e).__name__}:{func.__name__}"

            if not DEBUG:
                raise

            if not os.path.exists('logs/'):
                os.mkdir('logs/')

            with open(f"logs/{file_name}", "a") as log_file:
                log_file.write(f"Exception thrown, {type(e)}: {str(e)}\n")
                frames = inspect.getinnerframes(sys.exc_info()[2])
                for frame_info in reversed(frames):
                    f_locals = frame_info[0].f_locals
                    if "__lgw_marker_local__" in f_locals:
                        continue

                    log_file.write(f"File{frame_info[1]},"
                                   f"line {frame_info[2]}"
                                   f" in {frame_info[3]}\n"
                                   f"{     frame_info[4][0]}\n")

                    for k, v in f_locals.items():
                        log_file.write(f"    {k} = {log_to_str(v)}\n")
                log_file.write("\n")

            raise

    return wrapper
