import unittest
from logics import Logics


class TestLogics(unittest.TestCase):
    def test_get_balanced_tp(self):
        supply = [20, 30]
        demand = [10, 20, 30]
        costs = [[1, 2, 3], [4, 5, 6]]
        penalties = [7, 8]

        balanced_supply, balanced_demand, balanced_costs = Logics.get_balanced_tp(
            supply, demand, costs, penalties)

        self.assertEqual(balanced_supply, [20, 30, 0])
        self.assertEqual(balanced_demand, [10, 20, 30])
        self.assertEqual(balanced_costs, [[1, 2, 3], [4, 5, 6], [7, 8, 0]])

    def test_north_west_corner(self):
        supply = [20, 30]
        demand = [10, 20, 30]

        bfs = Logics.north_west_corner(supply, demand)

        self.assertEqual(len(bfs), 4)
        self.assertEqual(bfs[0], ((0, 0), 10))
        self.assertEqual(bfs[1], ((0, 1), 10))
        self.assertEqual(bfs[2], ((1, 0), 20))
        self.assertEqual(bfs[3], ((1, 1), 10))

    def test_get_vs_and_ws(self):
        bfs = [((0, 0), 10), ((0, 1), 10), ((1, 0), 20), ((1, 1), 10)]
        costs = [[1, 2], [3, 4]]

        vs, ws = Logics.get_vs_and_ws(bfs, costs)

        self.assertEqual(vs, [0, 1])
        self.assertEqual(ws, [1, 0])

    def test_get_cs(self):
        bfs = [((0, 0), 10), ((0, 1), 10), ((1, 0), 20), ((1, 1), 10)]
        costs = [[1, 2], [3, 4]]
        vs = [0, 1]
        ws = [1, 0]

        cs = Logics.get_cs(bfs, costs, vs, ws)

        self.assertEqual(len(cs), 0)

    def test_can_be_improved(self):
        cs = [((0, 0), 1), ((1, 0), 0), ((1, 1), 1)]

        self.assertTrue(Logics.can_be_improved(cs))

    def test_get_entering_variable_position(self):
        cs = [((0, 0), 1), ((1, 0), 0), ((1, 1), 1)]

        ev_position = Logics.get_entering_variable_position(cs)

        self.assertEqual(ev_position, (0, 0))

    def test_get_possible_next_nodes(self):
        loop = [(0, 0), (0, 1)]
        not_visited = [(0, 2), (1, 0), (1, 1), (1, 2)]

        possible_next_nodes = Logics.get_possible_next_nodes(loop, not_visited)

        self.assertEqual(possible_next_nodes, [(1, 0), (1, 1)])

    def test_get_loop(self):
        bv_positions = [(0, 0), (0, 1), (1, 1), (2, 0), (2, 1)]
        ev_position = (0, 1)

        loop = Logics().get_loop(bv_positions, ev_position)

        self.assertEqual(len(loop), 4)

    def test_get_total_cost(self):
        costs = [[1, 2], [3, 4]]
        solution = [[1, 0], [0, 1]]

        total_cost = Logics.get_total_cost(costs, solution)

        self.assertEqual(total_cost, 5)


if __name__ == '__main__':
    unittest.main()
