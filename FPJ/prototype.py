from os import system



def north_west_corner(supply: list[int], demand: list[int]) -> list[tuple[tuple[int], int]]:
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


def get_possible_next_nodes(loop, not_visited):
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

def get_loop(bv_positions, ev_position):
    def inner(loop):
        if len(loop) > 3:
            can_be_closed = len(
                get_possible_next_nodes(loop, [ev_position])) == 1
            if can_be_closed:
                return loop

        not_visited = list(set(bv_positions) - set(loop))
        possible_next_nodes = get_possible_next_nodes(loop, not_visited)
        for next_node in possible_next_nodes:
            new_loop = inner(loop + [next_node])
            if new_loop:
                return new_loop

    return inner([ev_position])


def cls():
    system('cls || clear')


def print_2d_array(data):
    max_x = max(coord[0] for coord in data)
    max_y = max(coord[1] for coord in data)

    array_2d = [[0] * (max_y + 1) for _ in range(max_x + 1)]

    for coord, value in data.items():
        x, y = coord
        array_2d[x][y] = value

    for row in array_2d:
        print(f'[ {", ".join("{:4}".format(value) for value in row)} ]')
        

def numeric_to_letter(numeric_y):
    return chr(65 + numeric_y)


def print_coordinate_val(data):
    for (x, y), value in data:
        letter_y = numeric_to_letter(y)
        print(f"({x+1},{letter_y}) = {value}")


def list_coordinates(data):
    return [coord for coord, value in data.items() if value != 0]


def list_missing_coordinates(data):
    return [coord for coord, value in data.items() if value == 0]


def compute_running_cost(data, costs):
    total = 0
    non_zero_data = {coord: value for coord, value in data.items() if value != 0}
    for coord, value in non_zero_data.items():
        x, y = coord
        product = value * costs[x][y]
        total += product
        # print(f"{x+1}-{numeric_to_letter(y)}    {value} × {costs[x][y]}") # PRINT_SOLUTION
    # print(f"costs = {total}")
    return total




def compute_for_improvement(coords, miscoords, costs):
    weight = {}
    for coord in miscoords:
        solution = ""
        total = 0
        loop = get_loop(coords, coord)
        multiplier = 1  
        for node in loop:
            x, y = node
            cost = costs[x][y] * multiplier
            total += cost
            if multiplier == 1:
                solution += f"+{cost}"
            else:
                solution += f"{cost}"
            multiplier *= -1  
        solution = solution[1:]
        solution = solution.replace('-', ' - ')
        solution = solution.replace('+', ' + ')
        # print(f"{coord[0]+1}-{numeric_to_letter(coord[1])}: {solution} = {total}") # PRINT_SOLUTION
        weight[coord] = total
    return weight

def print_dictionary(vac_cell):
    for coord, value in vac_cell.items():
        print(f"   {coord}: {value}")


def get_most_negative(vac_cell):
    most_negative_key = min(vac_cell, key=vac_cell.get)
    if vac_cell[most_negative_key] < 0:
        return most_negative_key
    else:
        return None


def complete_data(data):
    max_x = max(coord[0] for coord, _ in data)
    max_y = max(coord[1] for coord, _ in data)
    complete_data = {coord: 0 for coord in [(x, y) for x in range(max_x + 1) for y in range(max_y + 1)]}
    complete_data.update(dict(data))
    return complete_data


def is_zero(num):
    return True if (num % 2 == 0) else False


def is_one(num):
    return True if (num % 2 == 1) else False
        

def optimize_table(loop, full_data):
    transfer = float('inf')
    for i in range(len(loop)):
        coord = loop[i]
        if is_one(i):
            if full_data[coord] < transfer:
                transfer = full_data[coord]

    for i in range(len(loop)):
        coord = loop[i]
        if is_zero(i):
            full_data[coord] += transfer
        elif is_one(i):
            full_data[coord] -= transfer
    return full_data

def print_shipments(data):
    for coord, value in data.items():
        print(f"Plant {coord[0] + 1} to Project {numeric_to_letter(coord[1])}    ->    {value} truckloads")

def print_decision(data):
    non_zero_data = {coord: value for coord, value in data.items() if value != 0}
    print_shipments(non_zero_data)


if __name__ == "__main__":
    pass
