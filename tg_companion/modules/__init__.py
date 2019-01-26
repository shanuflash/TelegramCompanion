from tg_companion import LOGGER


def __list_modules__():
    from os.path import dirname, basename, isfile
    import glob

    path = glob.glob(dirname(__file__) + "/*.py")

    modules = [
        basename(f)[:-3]
        for f in path
        if isfile(f) and f.endswith(".py") and not f.endswith("__init__.py")
    ]

    return modules


MODULES = sorted(__list_modules__())
LOGGER.info("MODULES to load: %s ", str(MODULES))
__all__ = MODULES + ["MODULES"]
