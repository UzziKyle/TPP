import os
import numpy as np
import pprint
from .logics import Logics
from typing import List, Optional, Tuple


class Application:
    """
    A class to represent the application for solving transportation problems.

    Attributes:
    LOGIC_HANDLER (Logics): An instance of the Logics class for handling transportation problem logic.
    """

    LOGIC_HANDLER: Logics = Logics()

    def run(self) -> None:
        """
        Runs the application to solve a transportation problem.
        """
        self.clear_console()
        print("Hello, pangit!")

        supply: List[int] = self.get_input("Enter supplies: ")
        demand: List[int] = self.get_input("Enter demands: ")
        costs: List[List[int]] = self.get_matrix_input("Enter costs: ")

        solution: np.ndarray = self.transportation_simplex_method(
            supply, demand, costs)

        print(solution)
        print(
            f"Total Cost: {self.LOGIC_HANDLER.get_total_cost(costs, solution)}")

    def clear_console(self) -> None:
        """
        Clears the console screen.
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_input(self, message: str) -> List[int]:
        """
        Prompts the user for input and returns a list of integers.

        Args:
        message (str): The message to display to the user.

        Returns:
        List[int]: A list of integers entered by the user.
        """
        user_input: str = input(message)
        return [int(x.strip()) for x in user_input.split(',')]

    def get_matrix_input(self, message: str) -> List[List[int]]:
        """
        Prompts the user for matrix input and returns a matrix.

        Args:
        message (str): The message to display to the user.

        Returns:
        List[List[int]]: A matrix entered by the user.
        """
        rows: str = input(message)
        return [list(map(int, row.strip().split(','))) for row in rows.split(';')]

    def transportation_simplex_method(self, supply: List[int], demand: List[int], costs: List[List[int]], penalties: Optional[List[int]] = None) -> np.ndarray:
        """
        Solves a transportation problem using the simplex method.

        Args:
        supply (List[int]): List of supply values.
        demand (List[int]): List of demand values.
        costs (List[List[int]]): Cost matrix.
        penalties (Optional[List[int]], optional): List of penalties. Defaults to None.

        Returns:
        np.ndarray: The solution matrix.
        """
        balanced_supply, balanced_demand, balanced_costs = self.LOGIC_HANDLER.get_balanced_tp(
            supply, demand, costs
        )

        def inner(bfs: List[Tuple[Tuple[int, int], int]]) -> List[Tuple[Tuple[int, int], int]]:
            vs, ws = self.LOGIC_HANDLER.get_vs_and_ws(bfs, balanced_costs)
            cs = self.LOGIC_HANDLER.get_cs(bfs, balanced_costs, vs, ws)
            if self.LOGIC_HANDLER.can_be_improved(cs):
                ev_position = self.LOGIC_HANDLER.get_entering_variable_position(
                    ws)
                loop = self.LOGIC_HANDLER.get_loop(
                    [p for p, v in bfs], ev_position)
                return inner(self.LOGIC_HANDLER.loop_pivoting(bfs, loop))
            return bfs

        basic_variables = inner(self.LOGIC_HANDLER.north_west_corner(
            balanced_supply, balanced_demand))
        solution: np.ndarray = np.zeros((len(costs), len(costs[0])))
        for (i, j), v in basic_variables:
            solution[i][j] = v

        return solution
