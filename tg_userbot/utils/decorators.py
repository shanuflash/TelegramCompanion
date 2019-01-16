import asyncio

from tg_userbot import LOGGER, client


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
                            "The timer can't be lower than {} seconds".format(seconds)
                        )
                        quit(1)
                if max_value:
                    if seconds > max_value:
                        LOGGER.error(
                            "The timer can't be higher than {} seconds".format(seconds)
                        )
                        quit(1)
                while 1:
                    asyncio.ensure_future(fcn())
                    await asyncio.sleep(seconds)
            else:
                pass

        return wrapper

    return scheduler
