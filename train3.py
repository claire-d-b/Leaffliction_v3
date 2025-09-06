#!/usr/bin/env python3


from utils import load, normalize_df
from linear_regression import minimize_cost
from matplotlib.pyplot import savefig, clf, close, subplots
from pandas import concat, read_csv, set_option
from seaborn import pairplot
from sys import argv
import random
from glob import glob
import seaborn as sns


def train():
    """Plot the scores per course and classify"""

    csv_files = glob("features_Train_*.csv")
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
        print("df")
        print(df)
        print("index")
        print(i)
        dfs.append(df)

    combined_df = concat(dfs, ignore_index=True)
    combined_df.to_csv("features.csv")
    origin_df = load("features.csv")

    classes = sorted(list(set(origin_df['Category'])))
    ncolors = ['red', 'blue', 'green', 'gray', 'pink',
                   'purple', 'cyan', 'lightgreen']
    n = len(classes)

    # Get 3 random values without replacement
    random_colors = random.sample(ncolors, n)
    nmarkers = ['o', 's', 'X', 'D', 'o', 's', 'D', 'X']
    n = len(classes)

    # Get 3 random values without replacement
    random_markers = random.sample(nmarkers, n)

    df_class = origin_df.iloc[:, [2]]
    df_values = origin_df.iloc[:, 4:]

    # # Normalization
    # min_values = df_course.get_min()
    # max_values = df_course.get_max()
    # # -> résultats entre -1 et 1
    # df_course = df_course.apply(lambda col: normalize_column(col,
    #                             min_values[col.name], max_values[col.name]))
    df_values = normalize_df(df_values)
    print("dfvals", df_values)

    df = concat([df_class, df_values], axis=1)
    df = df.fillna(0)
    # ndf = df.reset_index()

    fig, ax = subplots()
    df = df.reset_index(drop=True)
    set_option('display.max_rows', None)
    set_option('display.max_columns', None)
    set_option('display.max_colwidth', None)
    set_option('display.width', None)
    set_option('display.expand_frame_repr', False)
    print("ici", df)

    sns.pairplot(df, hue="Category", palette=random_colors,
             markers=random_markers)
    savefig("output_class_I")
    # Clear the figure content
    clf()
    close()
    origin_df = origin_df.fillna(0)

    # df = df.sort_values(by='Category')

    print(f"Original df shape: {df.shape}")

    # print(f"Categories: {df['Category'].value_counts()}")
    print("classes", df)

    summed_df = df.groupby("Category", as_index=False).sum()
    print(f"Summed df shape: {summed_df.shape}")

    w = []
    b = []
    # Generate a random floating-point number between -0.01 and 0.01
    theta_0 = random.uniform(-0.01, 0.01)
    theta_1 = random.uniform(-0.01, 0.01)
    for i in range(len(classes)):
        w.insert(i, [])
        b.insert(i, [])
        # Scores of all students in the 13 courses for each house :
        # 4 lists of 13 values
        overall_scores = [item for sublist in summed_df[summed_df
                          ['Category'] == classes[i]].iloc[:, 1:].values
                          for item in sublist]
        # print("overall scores", overall_scores)
        # print("overall scores shape", DataFrame(overall_scores).shape)

        for j, item in enumerate(overall_scores):
            # print("i:", i)
            weight, bias, mse = minimize_cost(len(overall_scores),
                                              theta_0, theta_1,
                                              item, 1, 0.01)
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

    # pairplot(df, hue="Category", palette=random_colors,
    #          markers=random_markers)



if __name__ == "__main__":
    try:
        train()
    except AssertionError as error:
        print(f"{error}")