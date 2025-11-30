import logging
from collections import namedtuple
from datetime import datetime
from heapq import heapify, heappop, heappush
from pathlib import Path
from time import time_ns
from typing import Any, Callable, Literal

from aocd.models import Puzzle

from shared.logger import logger

Point = namedtuple("Point", ("y", "x"))

DIRECTIONS = {
    # dy , dx
    'down': Point(1, 0),
    'up': Point(-1, 0),
    'right': Point(0, 1),
    'left': Point(0, -1),
    'down-left': Point(1, -1),
    'down-right': Point(1, 1),
    'up-left':Point (-1, -1),
    'up-right': Point(-1, 1)
}


STRAIGHT_DIRECTIONS = {
    # dy , dx
    'down': Point(1, 0),
    'up': Point(-1, 0),
    'right': Point(0, 1),
    'left': Point(0, -1),
}

STRAIGHT_DIRECTIONS_SYMBOL = {
    # dy , dx
    'v': STRAIGHT_DIRECTIONS['down'],
    '^': STRAIGHT_DIRECTIONS['up'],
    '>': STRAIGHT_DIRECTIONS['right'],
    '<': STRAIGHT_DIRECTIONS['left']
}

DIAGONAL_DIRECTIONS = {
    # dy , dx
    'down-left': Point(1, -1),
    'down-right': Point(1, 1),
    'up-left': Point(-1, -1),
    'up-right': Point(-1, 1)
}
SMALL_LETTER = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')
CAPITAL_LETTER = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')
NUMBERS_STR = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')
NUMBERS_INT = (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)


def add_points(p1: Point, p2: Point) -> Point:
    """Add two Point instances by summing their coordinates."""
    return Point(
        y=p1.y + p2.y,
        x=p1.x + p2.x
    )

class Grid:
    def __init__(self, input_data: str, as_int: bool = False):
        """
        Initialize a Grid from input data.

        :param input_data: The input string representing the grid.
        :param parse_func: A function that takes a character and returns an integer.
                            Defaults to converting digits to integers, and leaves
                            other characters as strings.
        """
        self.grid = []
        for line in input_data.split('\n'):
            line = line.strip()  # Optionally remove leading/trailing whitespace
            if not line:
                break  # break at empty lines
            if as_int:
                self.grid.append([int(c) if c.isdigit() else None for c in line])
            else:
                self.grid.append([c for c in line])
        if self.grid and not all(len(row) == len(self.grid[0]) for row in self.grid):
            raise ValueError("All rows must have the same length")

    def __iter__(self):
        """
        Yield (y, x, cell_value) for each cell in the grid.
        """
        for y, row in enumerate(self.grid):
            for x, value in enumerate(row):
                yield y, x, value
    
    def __getitem__(self, p: Point) -> str | None:
        """
        Retrieve the parsed value at the given Point in the Grid.

        :param p: A Point instance with `y` and `x` attributes.
        :return: The parsed value at (p.y, p.x) if in bounds, otherwise None.
        """
        if self.in_bounds(p):
            return self.grid[p.y][p.x]
        return None
        
    def __setitem__(self, p: Point, value):
        """
        Set the value at the given Point in the Grid.
    
        :param p: A Point instance with `y` and `x` attributes.
        :param value: The value to set at (p.y, p.x).
        """
        if self.in_bounds(p):
            self.grid[p.y][p.x] = value      
     
    def __repr__(self):
        """
        Return a human-readable string representation of the grid.
        """
        return f"Grid:\n{self.to_string()}"
        
    def to_string(self) -> str:
        """
        Return a string representation of the grid, suitable for logging or printing.
        """
        if not self.grid:
            return ""        
        return '\n'.join(''.join(map(str, row)) for row in self.grid)

    def copy(self):
        """
        Create a deep copy of the Grid.
        """
        new_grid = Grid('')  # Create a new, empty Grid
        new_grid.grid = [row.copy() for row in self.grid]  # Deep copy of the grid data
        return new_grid

    @property
    def rows(self) -> int:
        """Get the number of rows in the grid."""
        return len(self.grid)

    @property
    def cols(self) -> int:
        """Get the number of columns in the grid."""
        return len(self.grid[0]) if self.grid else 0

    def in_bounds(self, p: Point) -> bool:
        """
        Check if the Point is within the bounds of the grid.

        :param p: A Point instance with `y` and `x` attributes.
        :return: True if the Point is within bounds, False otherwise.
        """
        return 0 <= p.y < self.rows and 0 <= p.x < self.cols

    def get_neighbors(self, p: Point, include_straight: bool = True, include_diagonal: bool = False) -> set:
        """
        Get all valid neighbors of a Point in the grid, based on direction settings.

        :param p: A Point instance with `y` and `x` attributes.
        :param include_straight: Include straight-direction neighbors (up, down, left, right).
        :param include_diagonal: Include diagonal-direction neighbors.
        :return: A set of `Point` objects representing valid neighboring positions.
        """
        directions = []
        if include_straight:
            directions.extend(STRAIGHT_DIRECTIONS.values())
        if include_diagonal:
            directions.extend(DIAGONAL_DIRECTIONS.values())
        if not directions:
            raise ValueError("include_straight or include_diagonal must be True")

        neighbors = set()
        for dy, dx in directions:
            neighbor = Point(p.y + dy, p.x + dx)
            if self.in_bounds(neighbor):
                neighbors.add(neighbor)
        return neighbors

class Graph:
    @staticmethod
    def add_edge(graph: dict, from_node: Any, to_node: Any, weight: int) -> None:
        graph.setdefault(from_node, {}) # Ensure from_node has an entry in the graph
        graph[from_node][to_node] = weight # Add/update the edge to to_node with its weight
        return None
    
    @staticmethod
    def get_shortest_paths(graph: dict, start_node: Any, destination_node: Any, return_all_paths: bool = False) -> tuple[list[list], int | None]:
        """
        Finds all shortest paths from the `start_node` to any graph node matching the `destination_node` in the grid. It leverages
        Dijkstra's algorithm and a backtracking step.
    
        Args:
            graph: The graph (adjacency list) containing all nodes.
            start_node: The initial node.
            destination_node: The target node (destination grid location).
            return_all_paths: when enabled, all shortest paths are returned (heavyly impacts performance) instead of just one.
    
        Returns:
            A tuple containing:
                - all_paths: A list of lists, where each inner list represents one
                             shortest path as a sequence of nodes.
                - lowest_cost: The minimum numerical cost to reach the `destination_node`,
                               or `None` if no path exists.
        """
        # First, run Dijkstra's to get the shortest path costs to all nodes
        # and a record of all predecessors that lead to those shortest paths.
        path_costs_for_each_node, predecessors = Graph._do_dijkstra(graph, start_node, return_all_paths=return_all_paths)
    
        # Filter for all nodes that are at the `destination_node` location and map them to their costs.
        end_nodes_to_cost_dict = {node: cost for node, cost in path_costs_for_each_node.items() if node == destination_node}
        # If no paths were found to the destination_node, or the lowest cost is still infinity, return empty.
        if not end_nodes_to_cost_dict or min(end_nodes_to_cost_dict.values()) == float('inf'):
            return [], None  # No path found
    
        lowest_cost = min(end_nodes_to_cost_dict.values())
        # Identify all specific end nodes that achieve this `lowest_cost`.
        # In this implementation there is only one, but there might be multiple such nodes if arriving at the destination_node from different
        # directions results in the same minimum total cost.
        end_nodes = [node for node, cost in end_nodes_to_cost_dict.items() if cost == lowest_cost]
    
        all_paths = []
    
        # For each identified `destination_node`, reconstruct all paths back to the `start_node`.
        for end_node in end_nodes:
            Graph._backtrack([end_node], all_paths, start_node, predecessors)
    
        return all_paths, lowest_cost
        
    @staticmethod
    def _do_dijkstra(graph: dict, start_node: Any, return_all_paths: bool = False) -> tuple[dict, dict]:
        """
        Executes Dijkstra's algorithm to find the shortest paths (and their costs)
        from a `start_node` to all other reachable nodes in a graph.
        It also records all predecessors for each node, allowing for reconstruction
        of multiple shortest paths if they exist.
    
        Args:
            graph: The adjacency list representation of the graph.
                   {node: {neighbor_node: weight}}.
            start_node: The starting node for Dijkstra's algorithm.
            return_all_paths: option to enable the search of all shortest paths
    
        Returns:
            A tuple containing:
                - path_costs_for_each_node: A dictionary mapping each node to its
                                            minimum accumulated cost from `start_node`.
                - predecessors: A dictionary mapping each node to a list of its
                                predecessor nodes on *all* shortest paths.
        """
        # Initialize costs: 0 for start_node, infinity for all others implicitly.
        path_costs_for_each_node = {start_node: 0}
        # Initialize predecessors: empty list for start_node.
        predecessors: dict[Any, list] = {start_node: []}
    
        # Initialize a min-priority queue with the start node and its cost.
        # The heap stores tuples of (cost, node).
        priority_queue = [(0, start_node)]
        heapify(priority_queue)
    
        while priority_queue:  # Continue as long as there are nodes to process
            current_weight, current_node = heappop(priority_queue)
    
            # If we've already found a shorter path to `current_node`, skip this (stale) entry.
            if current_weight > path_costs_for_each_node.get(current_node, float('inf')):
                continue
    
            # If the current node has no outgoing edges, it's a dead end in the graph, skip.
            if current_node not in graph:
                continue
    
            # Explore all neighbors of the current node.
            for neighbor, weight in graph.get(current_node, {}).items():
                # Calculate the total cost to reach the `neighbor` through `current_node`.
                tentative_cost = current_weight + weight
    
                # If this path offers a shorter cost to `neighbor` than previously known:
                if tentative_cost < path_costs_for_each_node.get(neighbor, float('inf')):
                    path_costs_for_each_node[neighbor] = tentative_cost # Update the shortest cost
                    predecessors[neighbor] = [current_node] # This is now the *only* known predecessor for this shortest path
                    heappush(priority_queue, (tentative_cost, neighbor)) # Add neighbor to priority queue
                # If this path offers an equally short cost:
                elif return_all_paths and tentative_cost == path_costs_for_each_node.get(neighbor, float('inf')):
                    predecessors.setdefault(neighbor, []).append(current_node) # Add current_node as an alternative predecessor
    
        return path_costs_for_each_node, predecessors
            
    @staticmethod
    def _backtrack(current_path: list, all_paths: list, start_node: Any, predecessors: dict):
        """
        Recursively reconstructs all shortest paths from an `destination_node` back to the
        `start_node` using the `predecessors` dictionary generated by Dijkstra's algorithm.
    
        Args:
            current_path: The path being built during the current recursive call.
                          It starts with the `destination_node` and grows backward.
            all_paths: A list that accumulates all fully reconstructed shortest paths.
            start_node: The designated starting node of the overall path.
            predecessors: The dictionary mapping nodes to a list of their predecessors
                          on shortest paths, as returned by `_do_dijkstra`.
        """
        last_visited_node = current_path[0] # The most recently added node to the current_path (which is the farthest from start)
        if last_visited_node == start_node:
            all_paths.append(current_path) # Base case: If we reached the start node, a full path is found.
            return
    
        if last_visited_node not in predecessors: # Safety check: If a node has no predecessors, it's an isolated part or error.
            return
    
        # For each predecessor of the `last_visited_node`, recursively call backtrack to extend the path.
        for predecessor in predecessors[last_visited_node]:
            Graph._backtrack([predecessor] + current_path, all_paths, start_node, predecessors)
    

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


def solve_puzzle_part(puzzle: Puzzle, solver_func: Callable, part: Literal['a', 'b'], example_data: bool = False, submit_solution: bool = True) -> str | None:
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
    if solution:
        solution = str(solution)
    else:
        return None
    end = time_ns()
    elapsed = (end - start) / 1e9
    if elapsed >= 1:
        formatted_time = f'{elapsed:.3f}s'
    elif elapsed >= 1e-3:
        formatted_time = f'{elapsed * 1e3:.3f}ms'
    else:
        formatted_time = f'{elapsed * 1e6:.3f}µs'
    logger.info(f'\033[1mAnswer part {part}: {solution}\033[22m')
    logger.info(f'Solution takes {formatted_time} to complete')
    if (solution and solution != 'None') and (logger.getEffectiveLevel() != logging.DEBUG) and submit_solution and (not example_data):
        setattr(puzzle, f'answer_{part}', solution)
    print()

    return solution


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


def flatten_list(list_to_flatten: list) -> list:
    return [x for sublist in list_to_flatten for x in (sublist if isinstance(sublist, list) else [sublist])]

#
# DEPRECATED
#

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
