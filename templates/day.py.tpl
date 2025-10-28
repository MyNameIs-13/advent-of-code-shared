#!/usr/bin/env python3
from aocd.models import Puzzle
from shared import utils
from shared.logger import logger
import logging
logger.setLevel(logging.DEBUG)  # comment out to disable debug logging real data

EXAMPLE_DATA = False
EXAMPLE_DATA = True  # comment out to use real data

def solve_part_a(input_data: str) -> str:
    # TODO: implement solution for part A
    result = None
    for line in utils.input_data_to_list(input_data):
        logger.debug(line)
    return str(result)


def solve_part_b(input_data: str) -> str:
    # TODO: implement solution for part B
    result = None
    for line in utils.input_data_to_list(input_data):
        logger.debug(line)
    return str(result)


def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day
    This is part of the template and does not need to be changed
    """
    year = {year}
    day = {day}
    logger.info(f'🎄 Running puzzle day {day:02}...')
    puzzle = Puzzle(year=year, day=day)
    input_data = utils.get_input_data(puzzle, example_data=EXAMPLE_DATA)

    utils.solve_puzzle_part(puzzle, solve_part_a, 'a', input_data, submit_solution=(not EXAMPLE_DATA))
    utils.solve_puzzle_part(puzzle, solve_part_b, 'b', input_data, submit_solution=(not EXAMPLE_DATA))

    return None

if __name__ == '__main__':
    main()