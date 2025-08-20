#!/usr/bin/env python3

from utils import load


def handle_distribution(path: str) -> None:
    distrib = load(path).T

    distrib = distrib.reset_index()
    distrib.columns = ['Subcategory', 'Category', 'Count']
    for i, scategory in enumerate(distrib.iloc[:, 0]):
        distrib.iloc[i, 0] = scategory[scategory.find('_')+1:]

    distrib = distrib.sort_values(by=['Subcategory', 'Count']).T
    tab = {}
    for key, count in zip(distrib.loc['Subcategory'], distrib.loc['Count']):
        if key in tab:
            tab[key] += count
        else:
            tab[key] = count


if __name__ == "__main__":
    try:
        handle_distribution("pictures.csv")
    except AssertionError as error:
        print(f"{error}")
