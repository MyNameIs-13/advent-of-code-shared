#!/usr/bin/env python3
from aocd.models import Puzzle
from shared import puzzle_helper
from shared.logger import logger
# import logging
# logger.setLevel(logging.DEBUG)

EXAMPLE_DATA = False
# EXAMPLE_DATA = True


def solve_part_a(input_data: str) -> str:
    # TODO: implement solution for part A
    pass

def solve_part_b(input_data: str) -> str:
    # TODO: implement solution for part B
    pass


def main() -> None:
    """
    Execute the solve functions for each part and submit the solution for the specified year and day
    This is part of the template and does not need to be changed
    """
    year = {year}
    day = {day}
    logger.info(f'🎄 Running puzzle day {day:02}...')
    puzzle = Puzzle(year=year, day=day)
    input_data = puzzle_helper.get_input_data(puzzle, example_data=EXAMPLE_DATA)

    for part, solve_func in [('a', solve_part_a), ('b', solve_part_b)]:
        puzzle_helper.solve_puzzle_part(puzzle, solve_func, part, input_data, example_data=EXAMPLE_DATA)

    return None

if __name__ == '__main__':
    main()