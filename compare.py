#!/usr/bin/env python3

from cv2 import imread, waitKey, destroyAllWindows, imwrite, resize, INTER_AREA, INTER_CUBIC, getRotationMatrix2D, warpAffine, convertScaleAbs, cvtColor, COLOR_BGR2HLS, COLOR_BGR2HSV, COLOR_BGR2RGB, medianBlur, getGaussianKernel, GaussianBlur, bilateralFilter, BORDER_CONSTANT, flip, COLOR_BGR2RGB, calcHist, COLOR_BGR2HLS, COLOR_BGR2HSV, split, COLOR_BGR2LAB
from matplotlib.pyplot import legend, imshow, axis, show, close, plot, title, xlabel, ylabel, savefig, ylim, figure, subplots
from sys import argv
from pathlib import Path
from numpy import float32, exp, ndarray
from glob import glob
from os import path
from pathlib import Path
from Transformation_types import get_hls, get_hsv, get_gaussian_blur, get_bilateral_filter, get_median_blurring_large_noise, get_median_blurring_small_noise
from pandas import DataFrame, option_context, read_csv
from utils import normalize_df, get_min, get_max, sort_list

def basic_comparison(file1, file2):
    """Basic comparison - shows differences between two CSV files"""
    print("=== BASIC COMPARISON ===")
    
    # Read CSV files
    df1 = read_csv(file1)
    df2 = read_csv(file2)
    
    print(f"File 1 shape: {df1.shape}")
    print(f"File 2 shape: {df2.shape}")
    
    # Check if columns are the same
    if list(df1.columns) == list(df2.columns):
        print("✓ Columns match")
    else:
        print("✗ Columns differ")
        print(f"File 1 columns: {list(df1.columns)}")
        print(f"File 2 columns: {list(df2.columns)}")
    
    # Check if data is identical
    if df1.equals(df2):
        print("✓ Files are identical")
    else:
        print("✗ Files differ")
        
        # Show different rows if same structure
        if df1.shape == df2.shape and list(df1.columns) == list(df2.columns):
            diff_mask = (df1 != df2).any(axis=1)
            diff_rows = df1[diff_mask].index.tolist()
            print(f"Different rows: {diff_rows}")
            print("length")
            print(f"{len(diff_rows)}")
            print("Accuracy rate")
            print(f"{round(100-len(diff_rows)*100/df1.shape[0], 2)}%")

if __name__ == "__main__":
    try:
        # basic_comparison("features_Test_Black_rot.csv", "Test/Test_Black_rot/Transformed/Test_Black_rot_Transformed_features_test.csv")
        basic_comparison("categories.csv", "categories_truth.csv")

    except AssertionError as error:
        print(f"{error}")
