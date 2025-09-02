#!/usr/bin/env python3

from sys import argv
from numpy import ndarray
from glob import glob
from os import path
from pathlib import Path
from Transformation_types import (get_hls, get_hsv, get_gaussian_blur,
                                  get_bilateral_filter,
                                  get_median_blurring_large_noise,
                                  get_median_blurring_small_noise,
                                  get_morphological_gradient, get_sobel,
                                  get_laplacian_operator, get_canny_edge,
                                  get_lab)
from Histogram import plot_multiple_images_histogram
from stats import get_len
from sys import argv


def process_file(src: str, dst: str, category: str, augmented: bool) \
                 -> ndarray | None:

    pattern = f"{dst}*"  # You can use *.png or *.* to match more
    # img = glob(pattern)
    # print("image")
    # print(img)
    # print("pattern")
    # print(pattern)
    true_subdir = "Histograms"

    ndst = f"{path.normpath(dst)}/{true_subdir}/"

    files = glob(f"{Path(pattern).parent}/{category}/*.JPG")
    # print("haha")
    # print(f"{dst}{category}/*.JPG")
    # print("files")
    # print(files)
    # print(f"{Path(pattern).parent}/{category}/*.JPG")
    plot_multiple_images_histogram(files, src, dst,
                                    ndst, category,
                                    augmented)

    return files


def process_input_transformation(src=None, dst=None, option=None, script=False) -> None:
    transformations = "lab", "hsv", "morphological_gradient", \
                      "bilateral_filter", "median_blur_small_noise", \
                      "canny_edge"
    if src and not src.endswith('/'):
        src = src + '/'
    if dst and not dst.endswith('/'):
        dst = src + '/'
    elif not dst:
        dst = src
    else:
        raise AssertionError("Please provide a path for files' transformation")
    img = None
    pattern = f"{src}Base/*.JPG"
    ndst = f"{src}"

    if src and path.isfile(src):
        ndst = f"{path.normpath(path.dirname(src))}/Histogram_subcategory/"

        if script:
            img = process_file(src, dst=ndst, category="Transformed",
                           augmented=False)
        get_lab(src, dst)
        get_hsv(src, dst)
        get_morphological_gradient(src, dst)
        get_bilateral_filter(src, dst)
        get_median_blurring_small_noise(src, dst)
        get_canny_edge(src, dst)

    else:
        folder = src
        # Try to find multiple files using glob pattern
        # Pattern for images starting with prefix
        img = glob(pattern)

        if img:
            print(f"Found {get_len(img)} files matching pattern: {pattern}")
            # plot_multiple_images_histogram(img, src, ndst)
            for i, image in enumerate(img):
                if script:
                    process_file(image, dst=dst, category="Transformed",
                             augmented=False)

                get_lab(image, dst)
                get_hsv(image, dst)
                get_morphological_gradient(image, dst)
                get_bilateral_filter(image, dst)
                get_median_blurring_small_noise(image, dst)
                get_canny_edge(image, dst)
        else:
            print(f"No files found matching pattern: {pattern}")


if __name__ == "__main__":
    try:
        match get_len(argv):
            case 1:
                raise AssertionError("Error: Please provide at least \
                                      one argument.")
            case 3:
                if argv[2] == "--script":
                    process_input_transformation(src=f"{argv[1]}/", script=True)
            case 5:
                if argv[1] == '-src' and argv[3] == '-dst':
                    process_input_transformation(src=argv[2], dst=argv[4])
                else:
                    raise AssertionError("Error: Unknown commmand: \
                                          see Augmentation.py -h (help).")
            case 7:
                if argv[1] == '-src' and argv[3] == '-dst' and \
                   argv[5] == '-options':
                    process_input_transformation(src=argv[2],
                                               dst=argv[4], option=argv[6])
            case _:
                raise AssertionError("Error: Too many arguments.")

    except AssertionError as error:
        print(f"{error}")
