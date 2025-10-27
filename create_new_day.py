#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path
from shared.logger import logger
from shared.misc_helper import get_day

def create_day(day: int) -> None:
    """
    Creates a new dayXX.py based on the day.py.tpl
    """
    # Get path information and check if file already exist
    aoc_repo_dir = Path(__file__).parent.parent
    template_file = aoc_repo_dir / 'shared' / 'templates' / 'day.py.tpl'
    aoc_dir = aoc_repo_dir / 'aoc'
    days_dir = aoc_dir / 'days'
    day_file = days_dir / f'day{day:02}.py'
    if day_file.exists():
        logger.error('File %s already exists. Aborting.', day_file)
        return None

    # Load template content and write day.py
    if not template_file.exists():
        raise FileNotFoundError(f'Missing template file: {template_file}')
    year = int(aoc_repo_dir.name.split('-')[-1])
    day_content = template_file.read_text().format(day=day, year=year)
    day_file.write_text(day_content)
    subprocess.run(['git', 'add', day_file], cwd=aoc_repo_dir, check=True)
    logger.info(f'Created day script: {day_file}')
    return None


if __name__ == '__main__':
    day_num = None
    # day_num = 1  # day overwrite
    day_num = get_day(sys.argv[1:], day_num)
    if day_num:
        create_day(day_num)
