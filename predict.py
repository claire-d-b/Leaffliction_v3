#!/usr/bin/env python3


from utils import load, normalize_df, open_thetas_file, get_max
from utils import get_dot
from matplotlib.pyplot import savefig, clf, close, figure, axhline, scatter
from matplotlib.pyplot import legend, gca
from pandas import concat
from seaborn import pairplot
from math import e
import ast
import random
from numpy import dot


def predict():
    origin_df = load("dataset_test.csv")
    norigin_df = load("dataset_test_truth.csv")
    df = origin_df.fillna(0)

    categories = sorted(list(set(norigin_df['Category'])))
    ncolors = ['red', 'blue', 'green', 'gray', 'pink', 'purple',
               'cyan', 'lightgreen']
    n = len(categories)

    # Get 3 random values without replacement
    random_colors = random.sample(ncolors, n)
    nmarkers = ['o', 's', 'X', 'D', 'o', 's', 'D', 'X']
    n = len(categories)

    # Get 3 random values without replacement
    random_markers = random.sample(nmarkers, n)

    # # origin_df = origin_df.reset_index(drop=False)
    # df_name = origin_df.iloc[:, :2]
    # df_values = origin_df.iloc[:, 2:]

    df = normalize_df(df)

    # df = concat([df_name, df_values], axis=1)

    bias, w = open_thetas_file("thetas.csv")
    bias = ast.literal_eval(bias)
    # Step 1: Use ast.literal_eval to safely parse the string as a 2D list
    parsed_data = ast.literal_eval(w)
    # Step 2: Convert each element to a float
    parsed_data = [[float(value) for value in row] for row in parsed_data]
    w = parsed_data

    # Make predictions based on computed thetas
    predictions = []
    # We iterate on x rows (transformed image) andy columns (values)
    # We make z predictions <=> probability that the leaf will
    # belong to each cetgory.
    # We take the highest probability.
    figure(figsize=(8, 5))
    # print("preuve")
    # print(df.iloc[:, 2:])
    # df = df.groupby('Subname').median(numeric_only=True)
    # print("dataframe")
    # print(df)
    # print(df.iloc[:, 4:])

    for i, col in enumerate(df.iloc[:, 4:].values):
        predictions.insert(i, [])
        # print("col", col)

        for j in range(len(categories)):
            z = dot(col, w[j]) + bias[j]

            predictions[i].insert(j, 1 / (1 + (e ** -z)))
            scatter(z, 1 / (1 + (e ** -z)),
                    color=random_colors[j % len(random_colors)],
                    marker='o', label=categories[j])

    # récupère tous les labels.
    handles, labels = gca().get_legend_handles_labels()
    # garde seulement un exemplaire de chaque label.
    by_label = dict(zip(labels, handles))
    # remplace la légende avec des labels uniques.
    legend(by_label.values(), by_label.keys())

    axhline(y=0.5, color='purple', linestyle='--',
            label="Seuil de décision (0.5)")
    savefig("output_scurve")
    clf()
    close()

    # predictions shape is (x, y) with values between 0 and 1.
    # Values upper than 0.5 indicates a probability that the leaf
    # will be in target class (categories[j]), whereas a < 0.5 value
    # tends to indicate the leaf belongs to another class.
    # when z is pos, the sigmoid function approches 1, whereas when
    # z is negative, the sigmoid function approaches 0.
    # From predictions get the highest value and corresponding house:

    # Remove only 2nd column values but keep column name
    # First, get the original column structure with 2nd column

    # from first file
    # Get 2nd column name:
    # third_column_name = col_df.columns[2]

    # Insert empty 2nd column back into the combined dataframe
    # Insert at position 1 with None values
    # df.insert(3, third_column_name, None)

    df['Category'] = [categories[p.index(get_max(p))] for p
                      in predictions]
    ndf = df
    # df = df.sort_values(by=['Name', 'Category', 'Modification'])
    # print(set(df['Category']))
    ncategories = categories

    ncolors = ['red', 'blue', 'green', 'gray', 'pink',
               'purple', 'cyan', 'lightgreen']
    n = len(ncategories)

    # Get 3 random values without replacement
    random_colors = random.sample(ncolors, n)
    nmarkers = ['o', 's', 'X', 'D', 'o', 's', 'D', 'X']
    n = len(ncategories)

    # Get 3 random values without replacement
    random_markers = random.sample(nmarkers, n)
    # df = df.sort_values(by='Name')
    # Write the entire DataFrame to a CSV file
    # df.sort_values(by='Category', ascending=False)
    first_col = df.iloc[:, [0]]
    last_col = df.iloc[:, [1]]
    res_df = concat([first_col, last_col], axis=1)
    # print("resdf")
    # print(res_df)
    res_df = res_df.sort_values(by='Subname')
    # res_df.groupby('Subname').median(numeric_only=True)

    res_df.to_csv("categories.csv", header=True, index=False)
    ftruth = load("dataset_test_truth.csv")

    # ffirst_col = ftruth.iloc[:, [0]]
    # flast_col = ftruth.iloc[:, [1]]
    # fdf = concat([ffirst_col, flast_col], axis=1)
    fdf = ftruth.sort_values(by='Subname').iloc[:, :2]

    # fdf.groupby('Subname').median(numeric_only=True)

    # ftruth.sort_values(by='Category', ascending=False)
    # ftruth = ftruth.sort_values(by=['Name', 'Category', 'Modification'])
    fdf.to_csv("categories_truth.csv", header=True, index=False)
    # df = df.sort_values(by='Category')
    df = df.iloc[:, 2:].groupby("Category").median(numeric_only=True)
    # print("DF")
    df = df.reset_index()
    # print(df)
    for i in range(len(ncategories)):
        filtered_df = df[df['Category'] == ncategories[i]]
        # print("filtered df")
        # print(filtered_df.values)
        percent = round(len(filtered_df) * 100 / len(df), 2)
        print(f"There are {percent}% students from test data \
who would probably belong to {ncategories[i]}")

    # index of category (0 to 3)
    # ncategories = [i for i, x in enumerate(ncategories)]

    pairplot(ndf, hue="Category", palette=[random_colors
                                           [i % len(random_colors)] for
                                           i in range(len(ncategories))],
             markers=random_markers)

    savefig("output_class_II")
    clf()
    close()


if __name__ == "__main__":
    try:
        predict()
    except AssertionError as error:
        print(f"{error}")
