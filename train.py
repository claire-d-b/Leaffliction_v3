#!/usr/bin/env python3

from utils import load, normalize_df
from linear_regression import minimize_cost
from matplotlib.pyplot import savefig, clf, close
from pandas import concat, read_csv
from seaborn import pairplot
from sys import argv
import random
import glob
from numpy import number

def train():
    csv_files = glob.glob("features_Train_*.csv")
    # print(csv_files)
    dfs = []
    for i, file in enumerate(csv_files):

        if i == 0:
            # First file: keep header
            df = read_csv(file)
        else:
            # Subsequent files: skip header (first row)
            df = read_csv(file, skiprows=1, header=None)
            # Use column names from the first dataframe
            df.columns = dfs[0].columns
        dfs.append(df)

    combined_df = concat(dfs, ignore_index=True)
    combined_df.to_csv("features.csv")

    categories = sorted(list(set(combined_df["Category"])))

    combined_df['Category'] = None
    combined_df.to_csv("features_test.csv")

    ncolors = ['red', 'blue', 'green', 'gray', 'pink',
                   'purple', 'cyan', 'lightgreen']
    n = len(categories)

    # Get 3 random values without replacement
    random_colors = random.sample(ncolors, n)
    nmarkers = ['o', 's', 'X', 'D', 'o', 's', 'D', 'X']
    n = len(categories)

    # Get 3 random values without replacement
    random_markers = random.sample(nmarkers, n)

    origin_df = load("features.csv")

    repr_df = origin_df.groupby("Subname").agg({
    'Category': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],  # Prend la première catégorie
    **{col: 'sum' for col in df.select_dtypes(include=[number]).columns}
    })

    repr_df = repr_df.reset_index()
    repr_df = normalize_df(repr_df)
    print(" rep df ")
    print(repr_df)
    origin_df = origin_df.fillna(0)

    df_class = origin_df.iloc[:, [2]]
    df_scores = origin_df.iloc[:, 4:]

    # # Normalization
    # min_values = df_course.get_min()
    # max_values = df_course.get_max()
    # # -> résultats entre -1 et 1
    # df_course = df_course.apply(lambda col: normalize_column(col,
    #                             min_values[col.name], max_values[col.name]))
    df_scores = normalize_df(df_scores)

    df = concat([df_class, df_scores], axis=1)

    df = df.sort_values(by='Category')

    summed_df = df.groupby("Category", as_index=False).median()

    w = []
    b = []
    # Generate a random floating-point number between -0.01 and 0.01
    theta_0 = random.uniform(-0.01, 0.01)
    theta_1 = random.uniform(-0.01, 0.01)
    for i in range(len(categories)):
        w.insert(i, [])
        b.insert(i, [])
        # Scores of all students in the 13 courses for each house :
        # 4 lists of 13 values
        overall_scores = [item for sublist in summed_df[summed_df
                          ['Category'] == categories[i]].iloc[:, 1:].values
                          for item in sublist]
        
        # print("overall scores shape", DataFrame(overall_scores).shape)

        for j, item in enumerate(overall_scores):
            # print("i:", i)
            weight, bias, mse = minimize_cost(len(overall_scores),
                                              theta_0, theta_1,
                                              item, 1, 0.00001)
            w[i].insert(j, weight)
            b[i].insert(j, bias)

    # Here we take the average value of ou bias
    # print("bias", b)
    bias = [sum(b_row) / len(b_row) for b_row in b]
    # print("bias", bias)
    
    # Write reusable thetas to a file
    f = open("thetas.csv", "w")
    thetas_1 = [[float(x) for x in row] for row in w]

    f.write(f"theta_0: {bias}\ntheta_1: {thetas_1}")
    f.close()

    # colors = {0: "red", 1: "yellow", 2: "blue", 3: "green"}
    # index of category (0 to 3)
    # categories = [i for i, x in enumerate(categories)]

    pairplot(repr_df, hue='Category', palette=[random_colors
                                           [i % len(random_colors)] for
                                           i in range(len(categories))],
             markers=random_markers)

    savefig("output_class_I")
    # Clear the figure content
    clf()
    close()


if __name__ == "__main__":
    try:
        train()
    except AssertionError as error:
        print(f"{error}")