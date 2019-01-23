import asyncio
from datetime import datetime
import sys
import os
import inspect
import functools
from tg_userbot import client, LOGGER, DEBUG


def timer(seconds=3600, min_value=None, max_value=None, run=True):
    """Run a decorated function every x seconds.

    The decorated function must be added as a task in the main file (see main for examples)

    seconds: [int] How many seconds to wait before re-executing the function.
    min_value: [int] The low limit of seconds allowed
    max_value: [int] The max limit of seconds allowed
    run: [bool] Default is True, set to False to stop the function from activating. [Usefull to use as a config var]
    """

    def scheduler(fcn):
        async def wrapper():
            while not client.is_connected():
                await asyncio.sleep(1)
            if run:
                if min_value:
                    if seconds < min_value:
                        LOGGER.error(
                            f"The timer can't be lower than {seconds} seconds"
                        )
                        quit(1)
                if max_value:
                    if seconds > max_value:
                        LOGGER.error(
                            f"The timer can't be higher than {seconds} seconds"
                        )
                        quit(1)
                while 1:
                    asyncio.ensure_future(fcn())
                    await asyncio.sleep(seconds)
            else:
                pass

        return wrapper

    return scheduler



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
