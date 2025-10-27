import logging
from pathlib import Path
from time import time_ns
from typing import Callable, Literal

from shared.logger import logger
from aocd.models import Puzzle

def get_input_data(puzzle: Puzzle, example_data: bool = False) -> str:
    """
    Get the user specific or example input data from the already existing file or from the website
    When getting data from website, save in file

    :param puzzle: puzzle data of specified day
    :param example_data: influences if the user specific data is returned or the example data for the day
    :return: puzzle input as string
    """
    logger.info('Loading puzzle data...')

    aoc_dir = Path(__file__).parent.parent / 'aoc'
    if example_data:
        input_data_file = aoc_dir / f'day{puzzle.day:02}_example.txt'
    else:
        input_data_file = aoc_dir / f'day{puzzle.day:02}.txt'
    if input_data_file.exists():
        input_data = input_data_file.read_text()
    else:
        if example_data:
            if puzzle.examples:
                input_data = puzzle.examples[0].input_data
            else:
                input_data = ''
        else:
            input_data = puzzle.input_data
        input_data_file.write_text(input_data)

    return input_data


def solve_puzzle_part(puzzle: Puzzle, solver_func: Callable, part: Literal['a', 'b'], input_data: str, submit_solution: bool = True) -> None:
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
    :param input_data: puzzle input as string
    :param submit_solution: influences if the solution is submitted
    :return: Nothing
    """
    start = time_ns()
    solution = solver_func(input_data)
    end = time_ns()
    elapsed = (end - start) / 1e9
    if elapsed >= 1:
        formatted_time = f'{elapsed:.3f} s'
    elif elapsed >= 1e-3:
        formatted_time = f'{elapsed * 1e3:.3f} ms'
    else:
        formatted_time = f'{elapsed * 1e6:.3f} µs'
    print()
    logger.info(f'\033[1mAnswer part {part}: {solution}\033[22m')
    logger.info(f'Solution takes {formatted_time} to complete')
    if (solution and solution != 'None') and (logger.getEffectiveLevel() != logging.DEBUG) and submit_solution and not (puzzle.answered(part)):
        setattr(puzzle, f"answer_{part}", solution)

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
