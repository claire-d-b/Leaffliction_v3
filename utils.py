#!/usr/bin/env python3

from pandas import DataFrame, read_csv


def get_housename(case_value, categories) -> str | None:
    """Defines 'true house' vs 'wrong houses'"""
    match case_value:
        case 0:
            return categories[0]
        case 1:
            return categories[1]
        case _:
            return None


def load(path: str) -> DataFrame:
    """Function that opens a file and display inner data in the shape
    of a datatable"""
    try:
        # Ici open est un gestionnaire de contexte qui retourne un
        # object-fichier
        file = read_csv(path, index_col=0)
        # file = file.fillna(0)

    except Exception as e:
        raise AssertionError(f"Error: {e}")
    return file


def open_thetas_file(name: str) -> tuple:
    theta_0 = 0
    theta_1 = []
    try:
        f = open(name, "r")
        file_content = f.read()

        index = file_content.find("theta_0:")
        i = index + len("theta_0:")
        theta_0 = file_content[i:file_content.find("\n")]

        index = file_content.find("theta_1:")
        i = index + len('\ntheta_1:')
        theta_1 = file_content[i:]

        return theta_0, theta_1
    except Exception as e:
        raise AssertionError(f"Error: {e}")


def get_min(df: DataFrame):
    nlst = sort_list(list(df))
    return nlst[0]


def get_max(df: DataFrame):
    nlst = sort_list(list(df))
    return nlst[len(nlst)-1]


def sort_list(sort_list: list):
    n = len(sort_list)
    for i in range(n):
        # Find the minimum element in the unsorted part of the list
        min_index = i
        for j in range(i + 1, n):
            if sort_list[j] < sort_list[min_index]:
                min_index = j
        # Swap the found minimum element with the first element
        sort_list[i], sort_list[min_index] = sort_list[min_index], sort_list[i]

    return sort_list


def normalize_df(df):
    # Normalisation linéaire des valeurs d'une colonne pour les transformer
    # en valeurs comprises entre -1 et 1.

    # (df[col] - col_min) : Cette partie soustrait la valeur minimale
    # de la colonne de chaque valeur, ce qui fait que la plus petite
    # valeur devient 0.
    # (col_max - col_min) : Calcule l'amplitude totale des valeurs dans
    # la colonne.
    # (df[col] - col_min) / (col_max - col_min) : Cette division
    # normalise les valeurs pour qu'elles soient toutes dans l'intervalle
    # [0, 1].
    # La valeur minimale est maintenant 0 et la valeur maximale est 1.
    # 2 * (...) : Multiplie toutes les valeurs par 2, ce qui transforme
    # l'intervalle en [0, 2].
    # 2 * (...) - 1 : Soustrait 1, ce qui déplace finalement l'intervalle
    # à [-1, 1].

    # Donc, en résumé, cette formule prend des données avec une plage
    # quelconque et les transforme pour qu'elles soient réparties
    # entre -1 et 1, où la valeur minimale d'origine devient -1 et la
    # valeur maximale d'origine devient 1.
    # Créer une copie du DataFrame pour ne pas modifier l'original
    normalized_df = df.copy()

    # Sélectionner uniquement les colonnes numériques
    numeric_columns = df.select_dtypes(include=float).columns

    for col in numeric_columns:
        # Calculer min et max de la colonne
        col_min = get_min(df[col])
        col_max = get_max(df[col])

        # Vérifier que min et max sont différents pour éviter division par zéro
        if col_max > col_min:
            # Formule de normalisation entre -1 et 1:
            # 2 * (x - min) / (max - min) - 1
            normalized_df[col] = 2*(df[col] - col_min)/(col_max - col_min)-1
        else:
            # Si toutes les valeurs sont identiques, on les met à 0
            normalized_df[col] = 0

    return normalized_df


def get_dot(lst: list, other: list):
    temp = []
    for index in range(len(lst)):
        temp.append(lst[index] * other[index])
    res = 0
    for index in range(len(lst)):
        res += temp[index]
    return res
