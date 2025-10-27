#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
import importlib
from shared.logger import logger
from shared.create_new_day import create_day
from shared.misc_helper import get_day
# import logging
# logger.setLevel(logging.DEBUG)


def __run_or_create_day(day: int):
    """
    When the file for the day exists, run it
    Otherwise create the file from the template
    """
    module_name = f'aoc.days.day{day:02}'
    try:
        module = importlib.import_module(module_name)
        module.main()
    except ModuleNotFoundError:
        logger.warning(f'❌ Day {day:02} not found. Creating from template...')
        create_day(day)


if __name__ == '__main__':
    day_num = None
    # day_num = 1  # day overwrite
    day_num = get_day(sys.argv[1:], day_num)
    if day_num:
        __run_or_create_day(day_num)
