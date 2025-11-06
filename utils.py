import logging
from datetime import datetime
from pathlib import Path
from time import time_ns
from typing import Callable, Literal

from shared.logger import logger
from aocd.models import Puzzle

DIRECTIONS = {
    # dy , dx
    'down': (1, 0),
    'up': (-1, 0),
    'right': (0, 1),
    'left': (0, -1),
    'down-left': (1, -1),
    'down-right': (1, 1),
    'up-left': (-1, -1),
    'up-right': (-1, 1)
}

SMALL_LETTER = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
CAPITAL_LETTER = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
NUMBERS_STR = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')
NUMBERS_INT = (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)


def __get_input_data(puzzle: Puzzle, example_data: bool = False, part_b: bool = False) -> str:
    """
    Get the user specific or example input data from the already existing file or from the website
    When getting data from website, save in file

    :param puzzle: puzzle data of specified day
    :param example_data: influences if the user specific data is returned or the example data for the day
    :return: puzzle input as string
    """
    logger.info('Loading puzzle data...')

    inputs_dir = Path(__file__).parent.parent / 'aoc' / 'inputs'
    if example_data and part_b:
        input_data_file = inputs_dir / f'day{puzzle.day:02}_example_b.txt'
    elif example_data:
        input_data_file = inputs_dir / f'day{puzzle.day:02}_example.txt'
    else:
        input_data_file = inputs_dir / f'day{puzzle.day:02}.txt'
    if input_data_file.exists():
        input_data = input_data_file.read_text()
    else:
        if example_data:
            if puzzle.examples and len(puzzle.examples) > 1 and part_b:
                input_data = puzzle.examples[1].input_data
            elif puzzle.examples:
                input_data = puzzle.examples[0].input_data
            else:
                input_data = ''
        else:
            input_data = puzzle.input_data
        input_data_file.write_text(input_data)

    return input_data


def solve_puzzle_part(puzzle: Puzzle, solver_func: Callable, part: Literal['a', 'b'], example_data: bool = False, submit_solution: bool = True) -> None:
    """
    Execute the function and measures the needed time to solve the puzzle.
    Prints the solution and measured time
    Will submit the answer to the website in certain conditions
        solution must be filled and different from None
        loglevel is not DEBUG
        submit_solution is True
        puzzle part hasn't successful answered yet

    :param puzzle: puzzle data of specified day
    :param solver_func: function which should be used to determine the solution
    :param part: either 'a' or 'b'
    :param example_data: should the input data use the data from the examples
    :param submit_solution: influences if the solution is submitted
    :return: Nothing
    """
    if part == 'b' and (not puzzle.answered('a')):
        return None
    input_data = __get_input_data(puzzle, example_data, part_b=part == 'b')
    start = time_ns()
    solution = solver_func(input_data)
    end = time_ns()
    elapsed = (end - start) / 1e9
    if elapsed >= 1:
        formatted_time = f'{elapsed:.3f}s'
    elif elapsed >= 1e-3:
        formatted_time = f'{elapsed * 1e3:.3f}ms'
    else:
        formatted_time = f'{elapsed * 1e6:.3f}µs'
    print()
    logger.info(f'\033[1mAnswer part {part}: {solution}\033[22m')
    logger.info(f'Solution takes {formatted_time} to complete')
    if (solution and solution != 'None') and (logger.getEffectiveLevel() != logging.DEBUG) and submit_solution and (not example_data):
        setattr(puzzle, f'answer_{part}', solution)

    return None


def input_data_to_list(input_data: str, splitter: str = '\n') -> list:
    """
    Format the input_data into a list.
    without overwriting splitter, it will split the input_data into lines

    :param input_data: str with input
    :param splitter: character(s) at which the splits should occur
    :return: list of strings
    """
    return input_data.split(splitter)


def get_day(args, day_num: int | None) -> int | None:
    """
    Either use the provided day from parameter
     or provided day from shell arguments
     or today's date when in December
    Check if the day is in the advent range

    :param args: forwarded args from shell
    :param day_num: parameter to overwrite shell arguments and auto-detection
    :return: day when valid, None otherwise
    """
    if day_num:
        pass
    else:
        if len(args) >= 1:
            try:
                day_num = int(args[1])
            except ValueError:
                logger.error('Please provide a valid day number.')
                return None
        else:
            now = datetime.now()
            if now.month == 12:
                day_num = now.day
            else:
                logger.error('🗓️ Not December! Please specify a day manually.')
                return None
    if day_num in range(1, 25):
        return day_num
    else:
        logger.error('🗓️ Day not in range! Please specify a day manually.')
        return None


def get_grid(input_data: str) -> list:
    """
    Format an input string into a grid so that the rows and columns can be processed with x, y coordinates

    unfortunately list structures require to use y (rows) first
    rows = len(grid)
    cols = len(grid[0])
    for y in range(rows):
        for x in range(cols):
            c = grid[y][x]
            if c == '^':

    :param input_data: str with input
    :return: lists in list | rows and columns
    """
    grid = []
    for line in input_data.split('\n'):
        grid.append([c for c in line])
    return grid


def in_bounds(y: int, x: int, grid: list) -> bool:
    """
    Check if the provided grid location is inside the bounds of the grid

    :param y: y coordinate (row number) of the point in the grid that should be tested
    :param x: x coordinate (column  position) of the point in the grid that should be tested
    :param grid: the grid that should be checked
    :return: True when point is in bounds, False otherwise
    """
    rows = len(grid)
    cols = len(grid[0])
    return 0 <= y < cols and 0 <= x < rows

