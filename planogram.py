def planogram(fixture, products):
    """
    Arguments:
    - fixture :: DataFrame[["shelf_no", "shelf_width_cm"]]
    - products :: DataFrame[["product_id", "product_width_mm", "profit"]]

    Returns: DataFrame[["shelf_no", "product_id"]]
    """
    return fixture.join(products)[["shelf_no", "product_id"]]


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
