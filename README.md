The task is to place **products** into the **fixture**, maximizing product profit subject to the usual knapsack problem constraints:

-   **0/1 constraint:** there must be either zero or one of each product on the shelves
-   **shelf capacity constraint:** the sum of the product widths must not exceed the shelf width

`planogram.py` contains a minimal implementation.

To proceed:

1.  clone this repository
2.  **working on a new branch**, complete the implementation of `planogram.py:planogram()`.
    You are free to use your choice of additional libraries;
    make sure to update `pyproject.toml` / `requirements.txt` as necessary.
3.  get the code back to us:
    -   **private** repository on bitbucket (preferred) github, etc, or
    -   zip/tar project files and email us



# Planogram
The list of methods used:

* ```planogram()``` 
    - main function, generate result by using the functions defined below
    - input: fixture, products
    - output: result
    - terminology:
        - fixture &rightarrow; `DataFrame[["shelf_no", "shelf_width_cm"]]`
            - given input from csv data file
        - products &rightarrow; `DataFrame[["product_id", "product_width_mm", "profit"]]`
            - given input from csv data file
        - result &rightarrow; `DataFrame[["shelf_no", "product_id"]]`
            - output of the problem

* ```Upper_Bound_Func()``` 
    - find the upper bound of profit of the problem
    - input:
        - num_shelf
        - num_product
        - capacity_lst
        - product_lst
        - current_sol
        - current_shelf
        - current
    - output:
        - upper_bound
    - terminology:
        - num_shelf &rightarrow; `int`
            - number of shelf given
        - num_product &rightarrow; `int`
            - number of product given
        - capacity_lst &rightarrow; `list`
            - list converted from fixture
        - product_lst &rightarrow; `list`
            - list converted from products
        - current_sol &rightarrow; `list` of `list`
            - "matrix" containing all the current solutions <br />
            (a solution is indicated by either 0 [not inserted] or 1 [inserted], <br />to find out whether x<sup>th</sup> shelf has y<sup>th</sup> product, check current_sol[x][y])
        - current_shelf &rightarrow; `list` of `list`
            - list containing all the shelves <br />
            (a shelf is a list which contains the product [items of the product_lst])
        - current &rightarrow; `int`
            - indicator for the shelf that we are working on
        - upper_bound &rightarrow; `int`
            - upper bound of profit of the problem

* ```Lower_Bound_Func()``` 
    - find the lower bound of profit of the problem and associated solution
    - input:
        - num_shelf
        - num_product
        - capacity_lst
        - product_lst
        - current_sol
        - current_shelf
        - current
    - output:
        - lower_bound
        - tmp_current_sol
    - terminology:
        - lower_bound &rightarrow; `int`
            - lower bound of profit of the problem
        - tmp_current_sol &rightarrow; `list` of `list`
            - similar to current_sol, but only contains the solutions of knapsack()

* ```MTM_Bound_to_Bound()```
    - function that is built according to the journal </br>
    "A Bound and Bound algorithm for the zero-one multiple knapsack problem"
    - input:
        - num_shelf
        - num_product
        - capacity_lst
        - product_lst
    - output:
        - final_profit
        - final_sol
    - terminology:
        - final_profit &rightarrow; `int`
            - resulting profit of the problem
        - final_sol &rightarrow; `list` of `list`
            - similar to current_sol, but this is the resulting solution of the problem

* ```knapsack()```
    - single knapsack problem solution based on dynamic programming algorithm
    - input:
        - capacity
        - item
        - num_product
        - product_lst
    - output:
        - profit
        - sol
    - terminology:
        - capacity &rightarrow; `int`
            - constraint of the single knapsack (width of the shelf)
        - item &rightarrow; `list`
            - similar to product_lst, but may have less product due to the pop() function in Lower_Bound_Func
        - profit &rightarrow; `int`
            - resulting profit of the single knapsack problem
        - sol &rightarrow; `list`
            - similar to the structure of current_sol, but there is only a shelf here, thus is the resulting solution of the single knapsack problem# Alwin
