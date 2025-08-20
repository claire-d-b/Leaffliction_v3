#!/usr/bin/env python3

from matplotlib.pyplot import savefig, clf, close, figure, axhline, scatter
from matplotlib.pyplot import legend, gca, plot, ylabel, title, show, pie, cm, subplots, bar
import matplotlib.colors as mcolors
from pandas import concat, DataFrame, read_csv, Series
from numpy import linspace
from sys import argv
from pathlib import Path
from stats import get_len


def load_ret_dataframe(path: str) -> DataFrame:
    """Function that opens a file and display inner data in the shape
    of a datatable"""
    try:
        # Ici open est un gestionnaire de contexte qui retourne un
        # object-fichier sous forme de DataFrame
        file = read_csv(path, index_col=0)

    except Exception as e:
        raise AssertionError(f"Error: {e}")
    return file

def create_charts_from_dataframe(file: DataFrame, path: str) -> None:
    """Functions that makes various charts representing pictures'
    distribution"""
    exists = 0
    # not file.groupby("Category").empty
    for category, group in file.groupby("Category"):
        if category == path:

            category = group.columns
            labels = group.index
            count = group.values[:, 1]

            fig, ax = subplots()
            ax.pie(count.astype(float), labels=labels, autopct='%1.f%%')
            savefig(f"{set(group['Category'].values).pop()}/Distribution Pie")
            ax.clear()
            fig.clf()
            close(fig)

            fig, ax = subplots()
            ax.bar(labels, count.astype(float), label=labels, color=mcolors.TABLEAU_COLORS.values())
            ax.set_ylim(bottom=0)
            savefig(f"{set(group['Category'].values).pop()}/Distribution Bar")
            ax.clear()
            fig.clf()
            close(fig)

            exists = 1
    if exists == 0:
        raise AssertionError("Error: Category not found.")



if __name__ == "__main__":
    try:
        if get_len(argv) != 2:
            print("Error: Wrong number of arguments")
        else:
            data = load_ret_dataframe("pictures.csv")
            # transpose DataFrame
            data = data.T
            create_charts_from_dataframe(data, str(argv[1]).removeprefix("./"))
    except AssertionError as error:
        print(f"{error}")