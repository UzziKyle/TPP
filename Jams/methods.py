from typing import List, Tuple, Dict

class Logics:
    @staticmethod
    def get_balanced_tp(supply: list[int], demand: list[int], costs: list[list[int]], penalties: list[int] = None) -> tuple[list[int], list[int], list[list[int]]]:
        """
        Adjusts supply and demand to balance them if necessary and returns adjusted parameters.

        Args:
            supply (list[int]): List of supply values.
            demand (list[int]): List of demand values.
            costs (list[list[int]]): Cost matrix.
            penalties (list[int], optional): List of penalties. Defaults to None.

        Raises:
            Exception: When supply is less than demand and penalties are not provided.

        Returns:
            tuple[list[int], list[int], list[list[int]]]: Adjusted supply, demand, and costs.
        """
        total_supply = sum(supply)
        total_demand = sum(demand)

        if total_supply < total_demand:
            if penalties is None:
                raise Exception('Supply less than demand, penalties required')
            new_supply = supply + [total_demand - total_supply]
            new_costs = costs + [penalties]
            return new_supply, demand, new_costs
        if total_supply > total_demand:
            new_demand = demand + [total_supply - total_demand]
            new_costs = costs + [[0 for _ in demand]]
            return supply, new_demand, new_costs
        return supply, demand, costs

    @staticmethod
    def north_west_corner(supply: list[int], demand: list[int]) -> list[tuple[tuple[int], int]]:
        """
        Finds the initial basic feasible solution using the North-West Corner method.

        Args:
            supply (list[int]): List of supply values.
            demand (list[int]): List of demand values.

        Returns:
            list[tuple[tuple[int], int]]: Initial basic feasible solution.
        """
        supply_copy = supply.copy()
        demand_copy = demand.copy()
        i = 0
        j = 0
        bfs = []
        while len(bfs) < len(supply) + len(demand) - 1:
            s = supply_copy[i]
            d = demand_copy[j]
            v = min(s, d)
            supply_copy[i] -= v
            demand_copy[j] -= v
            bfs.append(((i, j), v))
            if supply_copy[i] == 0 and i < len(supply) - 1:
                i += 1
            elif demand_copy[j] == 0 and j < len(demand) - 1:
                j += 1
        return bfs

    @staticmethod
    def get_vs_and_ws(bfs: list[tuple[tuple[int], int]], costs: list[list[int]]) -> tuple[list[int], list[int]]:
        """
        Calculates the values of v and w in the Modified Distribution method.

        Args:
            bfs (list[tuple[tuple[int], int]]): Basic feasible solution.
            costs (list[list[int]]): Cost matrix.

        Returns:
            tuple[list[int], list[int]]: Values of v and w.
        """
        vs = [None] * len(costs)
        ws = [None] * len(costs[0])
        vs[0] = 0
        bfs_copy = bfs.copy()
        while len(bfs_copy) > 0:
            for index, bv in enumerate(bfs_copy):
                i, j = bv[0]
                if vs[i] is None and ws[j] is None:
                    continue

                cost = costs[i][j]
                if vs[i] is None:
                    vs[i] = cost - ws[j]
                else:
                    ws[j] = cost - vs[i]
                bfs_copy.pop(index)
                break

        return vs, ws

    @staticmethod
    def get_cs(bfs: list[tuple[tuple[int], int]], costs: list[list[int]], vs: list[int], ws: list[int]) -> list[tuple[tuple[int], int]]:
        """
        Calculates the costs of non-basic variables in the Modified Distribution method.

        Args:
            bfs (list[tuple[tuple[int], int]]): Basic feasible solution.
            costs (list[list[int]]): Cost matrix.
            vs (list[int]): List of v values.
            ws (list[int]): List of w values.

        Returns:
            list[tuple[tuple[int], int]]: Costs of non-basic variables.
        """
        cs = []
        for i, row in enumerate(costs):
            for j, cost in enumerate(row):
                non_basic = all([p[0] != i or p[1] != j for p, v in bfs])
                if non_basic:
                    cs.append(((i, j), vs[i] + ws[j] - cost))

        return cs

    @staticmethod
    def can_be_improved(cs: list[tuple[tuple[int], int]]) -> bool:
        """
        Checks if any cost of non-basic variables can be improved.

        Args:
            cs (list[tuple[tuple[int], int]]): Costs of non-basic variables.

        Returns:
            bool: True if any cost can be improved, False otherwise.
        """
        for p, v in cs:
            if v > 0:
                return True
        return False

    @staticmethod
    def get_entering_variable_position(cs: list[tuple[tuple[int], int]]) -> tuple[int, int]:
        """
        Finds the entering variable position with the highest cost.

        Args:
            cs (list[tuple[tuple[int], int]]): Costs of non-basic variables.

        Returns:
            tuple[int, int]: Entering variable position.
        """
        cs_copy = cs.copy()
        cs_copy.sort(key=lambda w: w[1])
        return cs_copy[-1][0]

    @staticmethod
    def get_possible_next_nodes(loop: list[tuple[int, int]], not_visited: list[tuple[int, int]]) -> list[tuple[int, int]]:
        """
        Finds possible next nodes in the loop for loop pivoting.

        Args:
            loop (list[tuple[int, int]]): Current loop.
            not_visited (list[tuple[int, int]]): Nodes not visited yet.

        Returns:
            list[tuple[int, int]]: Possible next nodes in the loop.
        """
        last_node = loop[-1]
        nodes_in_row = [n for n in not_visited if n[0] == last_node[0]]
        nodes_in_column = [n for n in not_visited if n[1] == last_node[1]]
        if len(loop) < 2:
            return nodes_in_row + nodes_in_column
        else:
            prev_node = loop[-2]
            row_move = prev_node[0] == last_node[0]
            if row_move:
                return nodes_in_column
            return nodes_in_row

    def get_loop(self, bv_positions: list[tuple[int, int]], ev_position: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Finds a loop containing the entering variable position.

        Args:
            bv_positions (list[tuple[int, int]]): Positions of basic variables.
            ev_position (tuple[int, int]): Entering variable position.

        Returns:
            list[tuple[int, int]]: Loop containing the entering variable position.
        """
        def inner(loop: list[tuple[int, int]]) -> list[tuple[int, int]]:
            if len(loop) > 3:
                can_be_closed = len(
                    self.get_possible_next_nodes(loop, [ev_position])) == 1
                if can_be_closed:
                    return loop

            not_visited = list(set(bv_positions) - set(loop))
            possible_next_nodes = self.get_possible_next_nodes(
                loop, not_visited)
            for next_node in possible_next_nodes:
                new_loop = inner(loop + [next_node])
                if new_loop:
                    return new_loop

        return inner([ev_position])

    @staticmethod
    def get_total_cost(costs: list[list[int]], solution: list[list[int]]) -> int:
        """
        Calculates the total cost of the solution.

        Args:
            costs (list[list[int]]): Cost matrix.
            solution (list[list[int]]): Solution matrix.

        Returns:
            int: Total cost of the solution.
        """
        total_cost = 0
        for i, row in enumerate(costs):
            for j, cost in enumerate(row):
                total_cost += cost * solution[i][j]
        return total_cost
    
    def loop_pivoting(self, bfs: List[Tuple[int]], loop: list[tuple[int, int]]) -> List[Tuple[int]]:
        even_cells = loop[0::2]
        odd_cells = loop[1::2]
        get_bv = lambda pos: next(v for p, v in bfs if p == pos)
        leaving_position = sorted(odd_cells, key=get_bv)[0]
        leaving_value = get_bv(leaving_position)
        
        new_bfs = []
        for p, v in [bv for bv in bfs if bv[0] != leaving_position] + [(loop[0], 0)]:
            if p in even_cells:
                v += leaving_value
            elif p in odd_cells:
                v -= leaving_value
            new_bfs.append((p, v))
        
        return new_bfs
    
    def transportation_simplex_method(self, supply: List[int], demand: List[int], costs: List[List[int]], penalties=None) -> List[Dict]:
        improvement = []
        balanced_supply, balanced_demand, balanced_costs = self.get_balanced_tp(
            supply, demand, costs
        )

        def inner(bfs):
            nonlocal improvement  # Access improvement variable from outer scope
            us, vs = self.get_vs_and_ws(bfs, balanced_costs)
            ws = self.get_cs(bfs, balanced_costs, us, vs)
            if self.can_be_improved(ws):
                ev_position = self.get_entering_variable_position(ws)
                loop = self.get_loop(self, [p for p, v in bfs], ev_position)

                temp_basic_var = bfs
                temp_solution = [[0 for _ in range(len(costs[0]))] for _ in costs]

                for (i, j), v in temp_basic_var:
                    temp_solution[i][j] = v

                cost = self.get_total_cost(balanced_costs, temp_solution)

                improvement.append({
                    "basic feasible solution": bfs,
                    "supply cost factors": us,
                    "demand cost factors": vs,
                    "entering variable": ev_position,
                    "close loop": loop,
                    "solution": temp_solution,
                    "cost": cost
                })

                return inner(self.loop_pivoting(self, bfs, loop))
            return bfs

        basic_variables = inner(self.north_west_corner(balanced_supply, balanced_demand))

        us, vs = self.get_vs_and_ws(basic_variables, balanced_costs)
        solution = [[0 for _ in range(len(costs[0]))] for _ in costs]
        for (i, j), v in basic_variables:
            solution[i][j] = v
        final_cost = self.get_total_cost(balanced_costs, solution)
        improvement.append({
            "basic feasible solution": basic_variables,
            "supply cost factors": us,
            "demand cost factors": vs,
            "entering variable": None,  
            "close loop": None,  
            "solution": solution,
            "cost": final_cost
        })

        return improvement

