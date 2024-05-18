from table import Modi_Matrix
import os

class Application:
    @staticmethod
    def user_input() -> None:
        prompt = "Modification Transportation Method \nEnter values in this following format:\nCosts - [cost1, cost2, cost3], [cost4, cost5, cost6] , ..., [costx, costy, costz]\nSupply/Demand - x1, x2, x3,..., xn"
        print(prompt)
        print()
        cost, supply, demand = Modi_Matrix.get_data()
        result = Modi_Matrix.get_result(cost=cost, supply=supply, demand=demand)
        output = Modi_Matrix.tabulate_result(supply=supply, demand=demand, result=result)
        
    @staticmethod
    def run() -> None:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            Application.user_input()
            
            choice = input("Do you want to continue? (y/n): ")
            if choice.lower() == 'n':
                break
            
if __name__ == "__main__":
    Application.run()
