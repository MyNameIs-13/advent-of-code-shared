# Advent of Code Shared

Contains centralized AoC Year generator and a shared library which is used as submodule in each year


## Year generator
- Usage from terminal:
    - python create_new_year.py <year> <init_git>
    - python create_new_year.py 2026 False
    - python create_new_year.py 2026
    - python create_new_year.py

- Creates:
    - New year repo folder advent-of-code-YYYY
    - Initializes new Git repo
    - Adds this repo as submodule named 'shared' to the new repo
    - Creates structure and files main.py, days/, inputs/ in new repo
    ```
    advent-of-code-YYYY/
    ├── .git/
    ├── .venv/ -> ./.venv
    ├── aoc/
    │   ├── days/
    │   │   └── __init__.py  
    │   ├── inputs/
    │   ├── __init__.py  
    │   └── run_or_create_day.py
    ├── shared/
    │   ├── __init__.py
    │   ├── create_new_day.py
    │   ├── logger.py
    │   ├── utils.py
    │   └── ...
    ├── .gitignore
    ├── requirements.txt
    └── README.md
    ```

## Shared
- Communication with AoC website based on https://github.com/wimglenn/advent-of-code-data
- token must be set in `~/.config/aocd_token` https://github.com/wimglenn/advent-of-code-wim/issues/1
- provides helper functions to solve puzzles faster i.e.:
  - template for each daily puzzle which can be create with create_new_day.py (shared) or run_or_create_day.py (aoc)
  - for more have a look to the templates/day.py.tpl and utils.py