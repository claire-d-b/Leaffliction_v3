#!/usr/bin/env python3


from utils import load, normalize_df, open_thetas_file, get_max
from utils import get_dot
from matplotlib.pyplot import savefig, clf, close, figure, axhline, scatter
from matplotlib.pyplot import legend, gca
from pandas import concat, DataFrame
from seaborn import pairplot
from math import e
import ast
import random
from numpy import number


def predict():
    df = load("features.csv")
    print("shape!")
    print(df.shape)
    print(df)
    ncats = df['Category']
    df = df.fillna(0)
    df_subname = df.iloc[:, [0]]
    df_class = df.iloc[:, [2]]
    df_values = df.iloc[:, 4:]
    df = concat([df_subname, df_class], axis=1)
    df = concat([df, df_values], axis=1)
    df = df.sort_values(by='Subname')

    df = df.groupby("Subname").agg({
    'Category': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],  # Prend la première catégorie
    **{col: 'sum' for col in df.select_dtypes(include=[number]).columns}
    })

    df = df.reset_index()
    print(df)
    classes = sorted(list(set(ncats)))
    print("REAL")
    print(df)
    print(df.shape)
    DataFrame(df.iloc[:, :2].to_csv("categories_truth.csv", header=True, index=False))

    ndf = load("features_test.csv")
    ndf = ndf.fillna(0)
    ndf['Category'] = None
    print("shape!")
    print(ndf.shape)
    print(ndf)

    # df_class = df['Category']
    ndf_subname = ndf.iloc[:, [0]]
    ndf_class = ndf.iloc[:, [2]]
    ndf_scores = ndf.iloc[:, 4:]

    ndf_scores = normalize_df(ndf_scores)
    ndf = concat([ndf_subname, ndf_class], axis=1)
    ndf["Category"] = None
    ndf = concat([ndf, ndf_scores], axis=1)

    print("hihiihi")
    print(ndf)

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

    # print("w:", w)
    # print("bias", bias)

    # Make predictions based on computed thetas
    predictions = []
    # print("ndf.iloc[:, 1:]", ndf.iloc[:, 1:])
    # We iterate on 400 rows (students) and 13 columns (courses)
    # We make 4 predictions <=> probability that the student will
    # belong to each house.
    # We take the highest probability.
    ncolors = ['red', 'blue', 'green', 'gray', 'pink', 'purple',
               'cyan', 'lightgreen']
    n = len(classes)

    # Get 3 random values without replacement
    random_colors = random.sample(ncolors, n)
    nmarkers = ['o', 's', 'X', 'D', 'o', 's', 'D', 'X']
    n = len(classes)

    # Get 3 random values without replacement
    random_markers = random.sample(nmarkers, n)
    print("et là ?")
    print(ndf.iloc[:, 2:])
    figure(figsize=(8, 5))
    for i, col in enumerate(ndf.iloc[:, 2:].values):
        predictions.insert(i, [])
        # print("col", col)

        for j in range(len(classes)):
            z = get_dot(col, w[j]) + bias[j]
            # print("z", z)
            # Le résultat z représente souvent un score ou une valeur avant
            # l'application d'une fonction d'activation.
            predictions[i].insert(j, 1 / (1 + (e ** -z)))
            # scatter(z, 1 / (1 + (e ** -z)), color=random_colors[j % len(random_colors)],
            #         marker='o', label=classes[j])

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

    # predictions shape is (400, 4) with values between 0 and 1.
    # Values upper than 0.5 indicates a probability that the student
    # will be in target class (houses[j]), whereas a < 0.5 value
    # tends to indicate the student belongs to another class.
    # when z is pos, the sigmoid function approches 1, whereas when
    # z is negative, the sigmoid function approaches 0.
    # From predictions get the highest value and corresponding house:
    # print("predictions", predictions)
    # print("predictions shape", DataFrame(predictions).shape)
    

    # Write the entire DataFrame to a CSV file
    print("on en est la")
    print(ndf.shape)
    ndf['Category'] = [classes[p.index(get_max(p))] for p
                             in predictions]
    print("after preds")
    print(ndf.shape)

    # ndf = ndf.fillna(0)
    # ndf_subname = ndf.iloc[:, [0]]
    # ndf_class = ndf.iloc[:, [2]]
    # ndf_values = ndf.iloc[:, 4:]
    # ndf = concat([ndf_subname, ndf_class], axis=1)
    # ndf = concat([ndf, ndf_values], axis=1)
    # ndf = ndf.sort_values(by='Subname')

    print("hoohoh")
    print(ndf)
    ndf = ndf.sort_values(by='Subname')

    ndf = ndf.groupby("Subname").agg({
        'Category': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],  # Prend la première catégorie prédite
        **{col: 'sum' for col in ndf.select_dtypes(include=[number]).columns}  
    })
    ndf = normalize_df(ndf)

    print("apres df")
    print(ndf)
    # ndf_subname = ndf.iloc[:, [0]]
    # ndf_class = ndf.iloc[:, [1]]
    # ndf_values = ndf.iloc[:, 2:]
    # ndf = concat([ndf_subname, ndf_class], axis=1)
    # ndf = concat([ndf, ndf_values], axis=1)
    # ndf = ndf.sort_values(by='Subname')
    # print("AND HERE")
    # print(ndf)
    # print("LA N2")
    # print(ndf)
    # ndf = ndf.groupby(["Subname", "Category"]).sum(numeric_only=True).reset_index()
    ndf = ndf.reset_index()
    print("lalala")
    print(ndf.iloc[:, :2])
    DataFrame(ndf.iloc[:, :2]).to_csv("categories.csv", header=True, index=False)
    

    for i in range(len(classes)):
        filtered_df = ndf[ndf['Category'] == classes[i]]
        percent = round(len(filtered_df) * 100 / len(ndf), 2)
        print(f"There are {percent}% students from test data \
who would probably belong to {classes[i]}")

    pairplot(ndf, hue="Category", palette=[random_colors
                                           [i % len(random_colors)] for
                                           i in range(len(classes))],
             markers=random_markers)

    savefig("output_class_II")
    clf()
    close()


if __name__ == "__main__":
    try:
        predict()
    except AssertionError as error:
        print(f"{error}")