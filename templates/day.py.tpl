#!/usr/bin/env python3
import logging
from typing import Any

from aocd.models import Puzzle

from shared import utils
from shared.logger import logger

logger.setLevel(logging.INFO)
EXAMPLE_DATA = False
SUBMIT = True

# HACK: Overwrites
# SUBMIT = False
logger.setLevel(logging.DEBUG)
EXAMPLE_DATA = True


def solve_part_a(input_data: str) -> Any:
    # TODO: implement solution for part A
    result = None
    for line in utils.input_data_to_list(input_data):
        logger.debug(line)
    return result


def solve_part_b(input_data: str) -> Any:
    # TODO: implement solution for part B
    result = None
    for line in utils.input_data_to_list(input_data):
        logger.debug(line)
    return result


def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day
    This is part of the template and does not need to be changed
    """
    year = {year}
    day = {day}
    logger.info('🎄 Running puzzle day {day:02}...')
    puzzle = Puzzle(year=year, day=day)

    part_a_solution = utils.solve_puzzle_part(puzzle, solve_part_a, 'a', example_data=EXAMPLE_DATA, submit_solution=SUBMIT)
    if part_a_solution is not None and part_a_solution != 'None':
        utils.solve_puzzle_part(puzzle, solve_part_b, 'b', example_data=EXAMPLE_DATA, submit_solution=SUBMIT)

    return None

if __name__ == '__main__':
    main()
