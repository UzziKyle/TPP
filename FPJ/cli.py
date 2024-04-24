from prototype import *


def get_data():
    try:
        cls() 
        print("Enter Data (comma separated)")
        supply = list(map(int, input("Supply: ").replace(' ', '').split(',')))
        demand = list(map(int, input("Demand: ").replace(' ', '').split(',')))

        if len(supply) != len(demand):
            print("\n !!!  Error: the Dimension should be EQUAL")
            input("\npress [ENTER] to continue...\n\n")
            get_data()
        else:
            costs = []
            print("\nEnter the following")
            for i in range(len(supply)):
                cost = list(map(int, input(f"Cost (row {i+1}): ").replace(' ', '').split(',')))
                costs.append(cost)
        return supply, demand, costs
    
    except ValueError:
        print("\n !!!  Error: Please enter valid data")
        input("\npress [ENTER] to continue...\n\n")
        get_data()
    




def main():
    # SAMPLE
    # supply = [158, 184, 179]
    # demand = [174, 204, 143]
    # costs = [
    #     [4, 8, 8],
    #     [16, 24, 16],
    #     [8, 16, 24]
    # ]


    supply, demand, costs = get_data()

    data = north_west_corner(supply=supply, demand=demand)
    full_data = complete_data(data)


    print("\nInitial Table:")
    print_2d_array(full_data)
    print()


    def try_optimizing(full_data, count=1):
        coords = list_coordinates(full_data)
        miscoords = list_missing_coordinates(full_data)


        # print('COMPUTATION FOR VACANT CELLS')
        improv = compute_for_improvement(coords, miscoords, costs)


        most_neg = get_most_negative(improv)
        if most_neg is None:

            print("\n\n\n  ~ ~ ~ FINAL ~ ~ ~  ")
            print("  ▼ ▼ ▼ TABLE ▼ ▼ ▼  \n")
            print_2d_array(full_data)
            print()
            print()
            print("Decision:")
            print_decision(full_data)
            min_cost = compute_running_cost(full_data, costs)
            print(f"\nMinimum Cost: ₱{min_cost}\n")
            return 


        most_nega_loop = get_loop(coords, most_neg)
        optimized_data = optimize_table(most_nega_loop, full_data)


        print(f"Table {count+1} (optimizing):")
        print_2d_array(optimized_data)
        print()
    


        # input('press [ENTER] to continue\n')
        # cls()
        try_optimizing(optimized_data, count+1)


    try_optimizing(full_data)


if __name__ == "__main__":
    main()