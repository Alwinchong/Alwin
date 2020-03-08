from __future__ import print_function

def planogram(fixture, products):
    """
    Arguments:
    - fixture :: DataFrame[["shelf_no", "shelf_width_cm"]]
    - products :: DataFrame[["product_id", "product_width_mm", "profit"]]

    Returns: DataFrame[["shelf_no", "product_id"]]
    """

    tmp_capacity_lst = fixture.to_numpy().tolist()
    capacity_lst = []
    for lst in tmp_capacity_lst:
        (index,width_cm) = lst
        capacity_lst.append([index,int(10*width_cm)])

    tmp_product_lst = products.to_numpy().tolist()
    product_lst = []
    for lst in tmp_product_lst:
        (index,width_mm,profit) = lst
        product_lst.append([index,int(width_mm),int(100*profit)])

    num_shelf = len(capacity_lst)
    num_product = len(product_lst)
    
    #Refer to the journal "A Bound and Bound algorithm for the zero-one multiple knapsack problem" on https://www.sciencedirect.com/science/article/pii/0166218X81900056
    (profit,result) = MTM_Bound_to_Bound(num_shelf,num_product,capacity_lst,product_lst)
    
    res_lst = []
    for shelf in range(len(result)):
        for product in range(len(result[shelf])):
            if result[shelf][product] == 1:
                res_lst.append([tmp_capacity_lst[shelf][0],tmp_product_lst[product][0]])

    return pd.DataFrame(res_lst,columns =["shelf_no", "product_id"])
    
    """
    #MTM bound to bound test (1,3,6),(4,5,9) 452
    capacity_lst = [[1,103],[2,156]]
    product_lst = [[1,18,78],[2,9,35],[3,23,89],[4,20,36],[5,59,94],[6,61,75],[7,70,74],[8,75,79],[9,76,80],[10,30,16]]
    num_shelf = 2
    num_product = 10
    print(MTM_Bound_to_Bound(num_shelf,num_product,capacity_lst,product_lst))
    """
    """
    #knapsack test (1,4,8) 1270
    capacity = 67
    product_lst = [[1,23,505],[2,26,352],[3,20,458],[4,18,220],[5,32,354],[6,27,414],[7,29,498],[8,26,545],[9,30,473],[10,27,543]]
    item = product_lst
    num_product = 10
    print(knapsack(capacity,item,num_product,product_lst))
    """

def Upper_Bound_Func(num_shelf,num_product,capacity_lst,product_lst,current_sol,current_shelf,current):

    sum_of_weight = 0
    for i in range(num_product):
        if product_lst[i] in current_shelf[current]:
            sum_of_weight += product_lst[i][1]*current_sol[current][i]

    other_capacity = 0
    for i in range(current+1,num_shelf):
        other_capacity += capacity_lst[i][1]

    capacity = capacity_lst[current][1]-sum_of_weight+other_capacity

    item = []
    for j in range(num_product):
        count = 0
        for i in range(current+1):
            count += current_sol[i][j]
        if count == 0:
            item.append(product_lst[j])

    (profit,sol) = knapsack(capacity,item,num_product,product_lst)

    upper_bound = 0
    for i in range(current+1):
        for j in range(num_product):
            if product_lst[j] in current_shelf[i]:
                upper_bound += product_lst[j][2]*current_sol[i][j]

    upper_bound += profit

    return upper_bound

def Lower_Bound_Func(num_shelf,num_product,capacity_lst,product_lst,current_sol,current_shelf,current):

    tmp_current_sol = []
    for i in range(num_shelf):
        tmp_current_sol.append([])
        for j in range(num_product):
            tmp_current_sol[i].append([])
            tmp_current_sol[i][j] = 0

    lower_bound = 0
    for i in range(current+1):
        for j in range(num_product):
            if product_lst[j] in current_shelf[i]:
                lower_bound += product_lst[j][2]*current_sol[i][j]
    
    item = []
    for j in range(num_product):
        count = 0
        for i in range(current+1):
            count += current_sol[i][j]
        if count == 0:
            item.append(product_lst[j])
    item = list(filter(lambda x: x not in current_shelf[current],item))

    sum_of_weight = 0
    for i in range(num_product):
        if product_lst[i] in current_shelf[current]:
            sum_of_weight += product_lst[i][1]*current_sol[current][i]    

    capacity = capacity_lst[current][1]-sum_of_weight

    indicator = current

    while (indicator < num_shelf):

        (profit,sol) = knapsack(capacity,item,num_product,product_lst)

        for i in range(num_product):
            tmp_current_sol[indicator][i] = sol[i]

        lower_bound += profit

        for i in range(num_product):
            if tmp_current_sol[indicator][i] == 1:
                item.remove(product_lst[i])

        indicator += 1

        capacity = capacity_lst[min(indicator,num_shelf-1)][1]

    return (lower_bound,tmp_current_sol)

def MTM_Bound_to_Bound(num_shelf,num_product,capacity_lst,product_lst):

    #Step 1: initialization
    current_shelf = []
    for i in range(num_shelf):
        current_shelf.append([])

    current_sol = []
    for i in range(num_shelf):
        current_sol.append([])
        for j in range(num_product):
            current_sol[i].append([])
            current_sol[i][j] = 0

    exact_sol = []
    for i in range(num_shelf):
        exact_sol.append([])
        for j in range(num_product):
            exact_sol[i].append([])
            exact_sol[i][j] = 0

    profit = 0
    current = 0

    U = Upper_Bound_Func(num_shelf,num_product,capacity_lst,product_lst,current_sol,current_shelf,current)
    UB = U

    #Step 2: heuristic
    def heuristic_step(current_shelf,current_sol,exact_sol,profit,current,U,UB):

        (L,tmp_current_sol) = Lower_Bound_Func(num_shelf,num_product,capacity_lst,product_lst,current_sol,current_shelf,current)

        if L > profit:
            profit = L

            for i in range(num_shelf):
                for j in range(num_product):
                    exact_sol[i][j] = current_sol[i][j]
            
            for i in range(current,num_shelf):
                for j in range(num_product):
                    if tmp_current_sol[i][j] == 1:
                        exact_sol[i][j] = 1

            if (profit == UB):
                return (profit, exact_sol)

            if (profit == U):
                return backtrack(current_shelf,current_sol,exact_sol,profit,current,U,UB)
    
        #Step 3: define new current solution
        while (current != num_shelf):

            tmp_set = {}
            for i in range(num_product):
                if tmp_current_sol[current][i] == 1:
                    tmp_set.update({i:product_lst[i]})

            while (len(tmp_set) != 0):

                index = min(tmp_set)
                product = tmp_set.pop(index)
                current_shelf[current].append(product)
                current_sol[current][index] = 1

                U = Upper_Bound_Func(num_shelf,num_product,capacity_lst,product_lst,current_sol,current_shelf,current)
                if U <= profit:
                    return backtrack(current_shelf,current_sol,exact_sol,profit,current,U,UB)
            
            current += 1

        current = num_shelf-1
        return backtrack(current_shelf,current_sol,exact_sol,profit,current,U,UB)

    #Step 4: backtrack
    def backtrack(current_shelf,current_sol,exact_sol,profit,current,U,UB):
        while (current != -1):

            while (len(current_shelf[current]) != 0):

                top_index = len(current_shelf[current])-1
                top_product = current_shelf[current][top_index]

                if (current_sol[current][product_lst.index(top_product)] == 0):
                    current_shelf[current].pop(top_index)

                else:
                    current_sol[current][product_lst.index(top_product)] = 0
                    U = Upper_Bound_Func(num_shelf,num_product,capacity_lst,product_lst,current_sol,current_shelf,current)

                    if U > profit:
                        return heuristic_step(current_shelf,current_sol,exact_sol,profit,current,U,UB)

            current -= 1
        
        print("Check the code, there is an error. (or perhaps there is no solution?)")
        return None

    (final_profit,final_sol) = heuristic_step(current_shelf,current_sol,exact_sol,profit,current,U,UB)

    return (final_profit,final_sol)

#Dynamic programming approach
def knapsack(capacity,item,num_product,product_lst):

    if len(item) <= 0 or capacity <= 0:
        sol = [0]*num_product
        return (0,sol)

    matrix = []
    for i in range(len(item)):
        matrix.append([])
        for j in range(capacity+1):
            matrix[i].append([])
            matrix[i][j] = 0

    sol = [0]*num_product

    for i in range(capacity+1):
        matrix[0][i] = 0

    for i in range(len(item)):
        for j in range(capacity+1):
            if item[i][1] > j:
                matrix[i][j] = matrix[i-1][j]
            else:
                matrix[i][j] = max(matrix[i-1][j],item[i][2]+matrix[i-1][j-item[i][1]])

    profit = matrix[len(item)-1][capacity]

    #either the result comes from the top matrix[i-1][total width]) or from (profit[i-1] + matrix[i-1][total width-width[i-1]]) in Knapsack table
    #if it comes from the latter one it means the item is included.

    width = capacity
    amount = profit
    
    for i in range(len(item)-1,-1,-1):
        if i == 0 and item[i][1] <= width:
            sol[product_lst.index(item[i])] = 1
        elif (amount <= matrix[i-1][width]):
            continue
        else:
            sol[product_lst.index(item[i])] = 1
            width = width - item[i][1]
            amount = amount - item[i][2]
            if width < 0 or amount < 0:
                break
    
    return (profit,sol)

if __name__ == "__main__":
    import numpy as np
    import pandas as pd

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--products",
        type=argparse.FileType(mode="r"),
        default="products.csv",
        help="products input file",
    )
    parser.add_argument(
        "--fixture",
        type=argparse.FileType(mode="r"),
        default="fixture.csv",
        help="fixture input file",
    )
    parser.add_argument(
        "--out", "-o", default="solution.csv", help="solution output file"
    )

    args = parser.parse_args()

    fixture = pd.read_csv(args.fixture)
    products = pd.read_csv(args.products)

    solution = planogram(fixture, products)

    solution.to_csv(args.out, index=False)

    print(
        "stats:",
        solution[["shelf_no", "product_id"]]
        .merge(fixture, on="shelf_no")
        .merge(products, on="product_id")
        .assign(n_products=1)
        .pivot_table(
            index=["shelf_no", "shelf_width_cm"],
            values=["n_products", "profit", "product_width_mm"],
            aggfunc=np.sum,
            margins=True,
        ),
        sep="\n",
    )

    #side note: construct a multidimensional matrix to solve the problem using dynamic programming is not feasible ==> array is too big
    """
    capacity_lst = list(map(lambda x: x[1],fixture.to_numpy().tolist())) #list of capacity
    product_lst = list(map(lambda x: (x[1],x[2]),products.to_numpy().tolist())) #list of tuple (width,profit)

    tup = (len(product_lst),)
    for i in range(len(capacity_lst)):
        tup += (int(10*capacity_lst[i]),)
    print(tup)
    dp = np.ndarray(tup).tolist()
    """