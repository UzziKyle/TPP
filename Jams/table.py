from typing import List, Dict, Tuple
from tabulate import tabulate
import ast
from methods import Logics
from typing import List

class Modi_Matrix:
    @staticmethod
    def get_data() -> Tuple[List[List[int]], List[int], List[int]]:
        """
        Getting user's input and checks if supply and demand are
        balanced or not.

        Returns:
            Tuple[List[List[int]], List[int], List[int]]: generated costs, supply, and demand
        """
        
        input_cost = input("Enter costs: ")
        sublists = input_cost.strip('[]').split("], [")
        cost = [list(ast.literal_eval(sublist)) for sublist in sublists]
        
        supply = list(map(int, input("Enter supply: ").strip().split(',')))
        demand = list(map(int, input("Enter demand: ").strip().split(',')))
        
        new_supply, new_demand, new_costs = Logics.get_balanced_tp(supply=supply, demand=demand, costs=cost)
        
        return new_costs, new_supply, new_demand
    
    @staticmethod
    def get_result(cost: List[List[int]], supply: List[int], demand: List[int]) -> List[Dict]:
        """
        Gets cost, supply, and demand values to perform MODI transportation method

        Args:
            cost (List[List[int]]): cost values
            supply (List[int]): supply values
            demand (List[int]): demand values
        Returns:
            List[Dict]: summary of MODI transportation method tables
        """
        result = Logics.transportation_simplex_method(Logics, supply=supply, demand=demand, costs=cost)
        return result
    
    
    def tabulate_result(supply: List[int], demand: List[int], result:List[Dict]) -> None:
        """
        Prints out a tabulated format of the result generated from MODI transportation process

        Args:
            supply (List[int]): supply values
            demand (List[int]): demand values
            result (List[Dict]): summary of MODI transportation method tables
        """
        supply_header = [chr(96 + i + 1).upper() for i in range(len(demand))]
        for i in range(2):
            supply_header.insert(0, ' ')
            
        demand_row = [i + 1 for i in range(len(supply))]
        supply_cf_header = [f'V{i + 1}' for i in range(len(supply))]
        demand_cf_row = [f'W{i + 1}' for i in range(len(demand))]
        
        for i, row in enumerate(result):
            print(f"Table {i + 1}\n")
            
            vs = [f"{supply_cf_header[i]} = {row["supply cost factors"][i]}" for i in range(len(row["supply cost factors"]))]
            print(vs)
            ws = [f"{demand_cf_row[i]} = {row["demand cost factors"][i]}" for i in range(len(row["demand cost factors"]))]
            print(ws)
            cur_table = row["solution"].copy()
            
            for i in range(len(cur_table)):
                cur_table[i].insert(0, vs[i])  
                cur_table[i].insert(1, demand_row[i])
                
            for i in range(2):
                ws.insert(0, ' ')
            
                
            cur_table.insert(0, ws)
            cur_table.insert(1, supply_header)
            
            
            entering_variable = f"{chr(96 + row["entering variable"][1] + 1).upper()}-{row["entering variable"][0] + 1}" if row["entering variable"] != None else None
            close_loop = [f"{supply_header[row["close loop"][i][1] + 2]}-{demand_row[row["close loop"][i][0]]}" for i in range(len(row["close loop"]))] if row["close loop"] else None
            cost = row["cost"]
                
            fmt_table = tabulate(tabular_data=cur_table, tablefmt="grid")
            
            print(fmt_table, '\n')
            print(f"Cost: {cost}\n")
            print(f"Entering variable: {entering_variable}\n")
            print(f"Close Loop: {close_loop}\n")
            print()
            
if __name__ == "__main__":
    pass