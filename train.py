#!/usr/bin/env python3


from utils import load, normalize_df
from linear_regression import minimize_cost
from matplotlib.pyplot import savefig, clf, close
from pandas import concat, read_csv
from seaborn import pairplot
from sys import argv
import random
import glob


def train():
    """Plot the scores per course and classify"""

    if len(argv) != 2:
        print("Give a folder path")
        return
    else:
        # pattern = f"**/*{argv[1]}_features_test.csv"
        # csv_files = glob.glob(pattern, recursive=True)
        # # print(files)
        # # print("arg")
        # # print(argv[1])
        # # print(f"./*/*/*_{argv[1]}_features_test.csv")
        # # csv_files = list(Path("./").glob(f"*_{argv[1]}_features_test.csv"))

        # # Combine files
        # # Combine files with only one header
        # dfs = []
        # for i, file in enumerate(csv_files):

        #     if i == 0:
        #         # First file: keep header
        #         df = read_csv(file)
        #     else:
        #         # Subsequent files: skip header (first row)
        #         df = read_csv(file, skiprows=1, header=None)
        #         # Use column names from the first dataframe
        #         df.columns = dfs[0].columns
        #     print("data")
        #     print(df)
        #     dfs.append(df)
        # print("dfs")
        # print(dfs)
        # Current directory
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
        print("combined df", combined_df)

        combined_df.to_csv("features.csv")

        # combined_df = concat([combined_df.iloc[:, :3],
        #                     combined_df.iloc[:, 3:]], axis=1)

        # Remove only 2nd column values but keep column name
        # First, get the original column structure with 2nd column
        # original_df = read_csv(csv_files[0])  # Get column structure
        # from first file
        # Get 2nd column name:
        # third_column_name = original_df.columns[2]
        # combined_df = combined_df.reset_index()
        combined_df['Category'] = None

        # Insert empty 2nd column back into the combined dataframe
        # Insert at position 1 with None values
        combined_df.to_csv("features_test.csv")

        origin_df = load("features.csv")
        df = origin_df.fillna(0)

        categories = sorted(list(set(df['Category'])))

        ncolors = ['red', 'blue', 'green', 'gray', 'pink',
                   'purple', 'cyan', 'lightgreen']
        n = len(categories)

        # Get 3 random values without replacement
        random_colors = random.sample(ncolors, n)
        nmarkers = ['o', 's', 'X', 'D', 'o', 's', 'D', 'X']
        n = len(categories)

        # Get 3 random values without replacement
        random_markers = random.sample(nmarkers, n)

        origin_df = df.reset_index(drop=True)

        # df_name = origin_df.iloc[:, [0]]
        df_subname = origin_df.iloc[:, [0]]
        # df_category = origin_df.iloc[:, [2]]
        # df_transformation = origin_df.iloc[:, [3]]
        df_category = origin_df.iloc[:, [2]]
        df_values = origin_df.iloc[:, 4:]
        # print("df vals")
        # df_values)
        df_values = normalize_df(df_values)

        # df = concat([df_name, df_subname], axis=1)
        # df = concat([df, df_category], axis=1)
        # df = concat([df, df_transformation], axis=1)
        df = concat([df_subname, df_category], axis=1)
        df = concat([df, df_values], axis=1)
        print("lololo")
        print(df)

        ppdf = df.copy()
        # ppdf = ppdf.sort_values(by='Subname') # groupby Name median
        # ppdf = ppdf.groupby(["Subname", "Category"]).median(numeric_only=True)
        # ppdf = ppdf.reset_index()
        # first_col = ppdf.iloc[:, [0]]
        # last_col = ppdf.iloc[:, 2:]
        # ppdf = concat([first_col, last_col], axis=1)

        # df = df.sort_values(by='Category')
        # df = normalize_df(df)
        # df = df.groupby("Category", as_index=False).sum(numeric_only=True)

        df = df.sort_values(by='Category')
        df = normalize_df(df)
        df = df.groupby("Category", as_index=False).sum(numeric_only=True)
        print("summed_df")
        print(df)

        w = []
        b = []
        # print("LALALA")
        # print(df.iloc[:, 1:])
        # Generate a random floating-point number between -0.01 and 0.01
        theta_0 = random.uniform(-0.0001, 0.0001)
        theta_1 = random.uniform(-0.0001, 0.0001)
        print("kest ?")
        print(df.iloc[:, 1:])

        for i in range(len(categories)):
            w.insert(i, [])
            b.insert(i, [])

            overall_values = [float(item) for sublist in df[df
                              ['Category'] == categories[i]].iloc[:, 1:].values
                              for item in sublist]
            print("overall")
            print(overall_values)
            print(categories[i])

            for j, item in enumerate(overall_values):

                weight, bias, mse = minimize_cost(len(overall_values),
                                                  theta_0, theta_1,
                                                  item, 1, 0.0001)
                w[i].insert(j, weight)
                b[i].insert(j, bias)

        bias = [sum(b_row) / len(b_row) if len(b_row) else 0 for b_row in b]

        # Write reusable thetas to a file
        f = open("thetas.csv", "w")
        thetas_1 = [[float(x) for x in row] for row in w]
        f.write(f"theta_0: {bias}\ntheta_1: {thetas_1}")
        f.close()

        # colors = {0: "red", 1: "blue", 2: "green", 3: "gray"}
        # index of category (0 to 3)
        # categories = [i for i, x in enumerate(categories)]

        pairplot(ppdf, hue='Category', palette=[random_colors
                                                [i]
                                                for i in range(len
                                                               (categories))],
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
