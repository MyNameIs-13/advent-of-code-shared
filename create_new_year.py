#!/usr/bin/env python3
import shutil
import sys
from datetime import datetime
from pathlib import Path
import subprocess
from logger import logger

# import logging
# logger.setLevel(logging.DEBUG)
SHARED_REPO_URL = 'https://github.com/MyNameIs-13/advent-of-code-shared.git'


def __create_new_year(year: int, initialize_git: bool = True) -> None:
    # Directory in which the advent-of-code-share repo is located
    shared_repo_parent_dir = Path(__file__).parent.parent
    new_aoc_repo_dir = shared_repo_parent_dir / f'advent-of-code-{year}'
    shared_venv = shared_repo_parent_dir / '.venv'
    venv_link = new_aoc_repo_dir / '.venv'

    if new_aoc_repo_dir.exists():
        logger.error('Directory %s already exists. Aborting.', new_aoc_repo_dir)
        return None

    try:
        logger.info('Create AoC %s repo structure', year)

        # ----------------------------------------------------------------
        # Create directories
        # ----------------------------------------------------------------
        logger.info('Create directories')
        aoc_dir = new_aoc_repo_dir / 'aoc'
        (aoc_dir / 'days').mkdir(parents=True)
        (aoc_dir / 'inputs').mkdir()

        # ----------------------------------------------------------------
        # Create files
        # ----------------------------------------------------------------
        logger.info('Create files')
        (aoc_dir / '__init__.py').touch()
        (aoc_dir / 'days' / '__init__.py').touch()

        # Load and write run_or_create_day.py from template
        template_file = shared_repo_parent_dir / 'advent-of-code-shared' / 'templates' / 'run_or_create_day.py.tpl'
        if not template_file.exists():
            raise FileNotFoundError(f'Missing template file: {template_file}')
        template_content = template_file.read_text()
        (aoc_dir / 'run_or_create_day.py').write_text(template_content)

        # Write README.md and .gitignore
        readme_text = [
            f'# Advent of Code {year}\n',
            'This repo contains my solutions for Advent of Code - https://adventofcode.com/\n',
            '## Interpreter\n',
            f'- This project uses shared venv at: {shared_venv}',
            '- Open this folder in PyCharm, then select the shared interpreter if symlink has not been created.'
        ]
        (new_aoc_repo_dir / 'README.md').write_text('\n'.join(readme_text))
        (new_aoc_repo_dir / '.gitignore').write_text('.idea/\n__pycache__/\ninputs/\n')
        (new_aoc_repo_dir / '.requirements.txt').write_text('advent-of-code-data==2.1.0')

        # ----------------------------------------------------------------
        # Initialize venv (allowed to fail)
        # ----------------------------------------------------------------
        if shared_venv.exists():
            if not venv_link.exists():
                venv_link.symlink_to(shared_venv, target_is_directory=True)
                logger.info(f'Linked shared venv: {venv_link} → {shared_venv}')
        else:
            logger.warning(f'Shared venv not found: {shared_venv}')

        # ----------------------------------------------------------------
        # Initialize git (optional)
        # ----------------------------------------------------------------
        if initialize_git:
            # Initialize Git and add shared repo
            logger.info('Creating new AoC year repo: %s', new_aoc_repo_dir)
            subprocess.run(['git', 'init'], cwd=new_aoc_repo_dir, check=True)
            logger.debug('Initialized Git repository')
            subprocess.run(['git', 'submodule', 'add', SHARED_REPO_URL, 'shared'], cwd=new_aoc_repo_dir, check=True)
            logger.debug('Added shared repo as submodule')
            subprocess.run(['git', 'add', '.'], cwd=new_aoc_repo_dir, check=True)
            subprocess.run(['git', 'commit', '-m', f'Initialize Advent of Code {year}'], cwd=new_aoc_repo_dir, check=True)

        logger.info('✅ AoC %s repo created', year)
        return None

    except Exception as e:
        logger.exception('❌ Error while creating AoC repo for %s', year)

        # ----------------------------------------------------------------
        # Rollback (remove partially created folder)
        # ----------------------------------------------------------------
        logger.warning('Rolling back changes...')
        try:
            if new_aoc_repo_dir.exists():
                shutil.rmtree(new_aoc_repo_dir)
                logger.warning('Rollback complete — removed %s', new_aoc_repo_dir)
        except Exception as cleanup_error:
            logger.exception('⚠️ Failed to clean up after error')


if __name__ == '__main__':
    init_git = True
    year_num = None
    year_num = 2025  # year overwrite
    if year_num:
        pass
    else:
        if len(sys.argv) >= 2:
            try:
                year_num = int(sys.argv[1])
            except ValueError:
                logger.error('Usage: python create_new_year.py <year>')
                logger.error('Please provide a valid year number.')
                sys.exit(1)
            if len(sys.argv) > 2:
                init_git = sys.argv[2] in ('True', True, 'Yes', 'yes', 'Y', 'y')
                logger.debug('Git initialization parameter evaluated to: %s', init_git)
        else:
            year_num = datetime.now().year
    __create_new_year(year_num, init_git)
