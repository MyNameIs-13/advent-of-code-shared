# Advent of Code Shared

Contains centralized AoC Year generator and a shared library which is used as submodule in each year


## Year generator
- Usage from terminal:
    - python create_new_year.py 2026 False
    - python create_new_year.py 2026
    - python create_new_year.py

- Creates:
    - New year repo folder advent-of-code-YYYY
    - Initializes new Git repo
    - Adds shared (this) repo as submodule to the new repo
    - Creates structure and files main.py, days/, inputs/ in new repo

## Shared
- Communication with AoC website based on https://github.com/wimglenn/advent-of-code-data
- token must be set in `~/.config/aocd_token` https://github.com/wimglenn/advent-of-code-wim/issues/1