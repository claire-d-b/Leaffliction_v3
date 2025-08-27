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

    # df_values = normalize_df(df_values)

    # df = concat([df_name, df_values], axis=1)

    print("ICI==>")
    print(df)

    bias, w = open_thetas_file("thetas.csv")
    print("bias")
    print(bias)
    print("w")
    print(w)
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
    print("here ?")
    print(df.iloc[:, 4:])
    for i, col in enumerate(df.iloc[:, 4:].values):
        predictions.insert(i, [])
        # print("col", col)
        # z_values = []
        for j in range(len(categories)):
            z = get_dot(col, w[j]) + bias[j]
            # z_values.append(z)

            predictions[i].insert(j, 1 / (1 + (e ** -z)))
            scatter(z, 1 / (1 + (e ** -z)),
                    color=random_colors[j % len(random_colors)],
                    marker='o', label=categories[j])
        # predicted_class = z_values.index(max(z_values))

        # print(predicted_class)
        # print("zvals")
        # print(z_values)
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
    print("haha")
    print(df)
    df['Category'] = [categories[p.index(get_max(p))] for p
                      in predictions]
    print("mdr")
    print(df)
    # ndf = df
    # ndf = ndf.sort_values(by='Subname') # groupby Name median
    ndf = df.sort_index()
    print("newdffff")
    print(ndf)

    # # ndf = ndf.groupby(["Subname", "Category"]).median(numeric_only=True)
    # print("haha")
    # print(ndf.values)
    # # ndf = ndf.sort_values(by='Subname') # groupby Name median

    # ndf = ndf.groupby(["Subname", "Category"]).median(numeric_only=True)
    # first_col = ndf.iloc[:, [0]]
    # cats = ndf.iloc[:, [2]]
    # vals = ndf.iloc[:, 2:]
    # print(vals)
    # ndf = concat([first_col, cats], axis=1)
    # ndf = concat([ndf, vals])
    print("iciiii")
    print(ndf)

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
    print("error ?")
    print(df)
    # res_df = df.sort_values(by='Subname') # groupby Name median
    # # res_df = res_df.groupby(["Subname", "Category"]).median(numeric_only=True)
    # print("LALALLA")
    # print(res_df)
    # cats = res_df["Category"]
    # res_df = res_df.groupby("Subname").median(numeric_only=True)
    # print("SHAPE")
    # print(res_df.shape)
    # res_df = res_df.reset_index()
    # print("resres")
    # print(res_df)
    # first_col = res_df.iloc[:, [0]]
    # # last_col = res_df.iloc[:, [1]]
    # res_df = concat([first_col, cats], axis=1)

    # res_df.groupby('Subname').median(numeric_only=True)
    df_pred = df.groupby("Subname").sum()
    # df_pred = df.groupby("Subname")["Category"].agg(lambda x: x.mode().iloc[0]).reset_index()
    df_pred.to_csv("categories.csv", index=False)

    # ffirst_col = ftruth.iloc[:, [0]]
    # flast_col = ftruth.iloc[:, [1]]
    # fdf = concat([ffirst_col, flast_col], axis=1)
    # fdf = ftruth.sort_values(by='Subname').iloc[:, 1:3]
    # ftruth = ftruth.sort_values(by='Subname') # groupby Name median
    # ncats = ftruth['Category']
    # ftruth = ftruth.groupby("Subname").median(numeric_only=True)
    # print("SHAPE")
    # print(ftruth.shape)
    # ftruth = ftruth.reset_index()
    # # res_df = res_df.groupby(["Subname", "Category"]).median(numeric_only=True)
    # first_col = ftruth.iloc[:, [0]]

    # ftruth = concat([first_col, ncats], axis=1)
    # fdf.groupby('Subname').median(numeric_only=True)
    dft_name = norigin_df['Subname']
    dft_cat = norigin_df['Category']
    dft_course = norigin_df.iloc[:, 4:]

    dft_course = normalize_df(dft_course)

    df_truth = concat([dft_name, dft_cat], axis=1)
    df_truth = concat([df_truth, dft_course], axis=1)
    # ftruth.sort_values(by='Category', ascending=False)
    # ftruth = ftruth.sort_values(by=['Name', 'Category', 'Modification'])
    # df_truth = norigin_df.groupby("Subname")["Category"].agg(lambda x: x.mode().iloc[0]).reset_index()
    df_truth.to_csv("categories_truth.csv", index=False)

    # df = df.sort_values(by='Category')
    # df = df.iloc[:, 2:].groupby("Category").median(numeric_only=True)
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
