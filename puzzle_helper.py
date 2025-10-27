import logging
from pathlib import Path
from time import time_ns
from typing import Callable, Literal

from shared.logger import logger
from aocd.models import Puzzle

def get_input_data(puzzle: Puzzle, example_data: bool = False) -> str:
    """
    Get the user specific input data
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


def solve_puzzle_part(puzzle: Puzzle, solver_func: Callable, part: Literal['a', 'b'], input_data: str, example_data: bool = False) -> None:
    """

    :param puzzle:
    :param solver_func:
    :param part:
    :param input_data:
    :param example_data:
    :return:
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
    if solution and (logger.getEffectiveLevel() != logging.DEBUG) and (not example_data) and not (puzzle.answered(part)):
        setattr(puzzle, f"answer_{part}", solution)

    return None


def input_data_to_list(input_data: str, splitter: str = '\n') -> list:
    """
    format the input_data into a list.
    without overwriting splitter, it will split the input_data into lines
    """
    return input_data.split(splitter)
