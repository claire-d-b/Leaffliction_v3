#!/usr/bin/env python3

from utils import load, normalize_df, open_thetas_file, get_max
from utils import get_dot
from matplotlib.pyplot import savefig, clf, close, figure, axhline, scatter
from matplotlib.pyplot import legend, gca
from pandas import concat, DataFrame, read_csv
from seaborn import pairplot
from math import e
import ast
import random

def handle_distribution(path: str) -> None:
    distrib = load(path).T

    distrib = distrib.reset_index()
    distrib.columns = ['Subcategory', 'Category', 'Count']
    for i, scategory in enumerate(distrib.iloc[:, 0]):
        distrib.iloc[i ,0] = scategory[scategory.find('_')+1:]

    distrib = distrib.sort_values(by=['Subcategory', 'Count']).T
    tab = {}
    for key, count in zip(distrib.loc['Subcategory'], distrib.loc['Count']):
        if key in tab:
            tab[key] += count
        else:
            tab[key] = count

    totals = {key: round(sum(float(x) for x in value.split()), 2) for key, value in tab.items()}
    # print(totals)
    maximum = get_max([value for key, value in totals.items()])
    # print(maximum)
    sample = [round((float(y)*100/maximum), 2) for x, y in totals.items()]
    # print(sample)


if __name__ == "__main__":
    try:
        handle_distribution("pictures.csv")
    except AssertionError as error:
        print(f"{error}")