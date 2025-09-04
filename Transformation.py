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
from matplotlib.pyplot import savefig, close, subplots, tight_layout, show
from cv2 import imread, imshow, imwrite
from pathlib import Path


def process_file(src: str, dst: str, category: str, augmented: bool) \
                 -> ndarray | None:

    pattern = f"{dst}*"  # You can use *.png or *.* to match more
    # img = glob(pattern)
    # print("image")
    # print(img)
    # print("pattern")
    # print(pattern)
    true_subdir = "Histograms"

    # ndst = f"{path.normpath(dst)}/{true_subdir}/"
    # print("this is the path")
    # print(f"{Path(src).parent.parent}/{category}/*.JPG")
    files = glob(f"{Path(src).parent.parent}/{category}/*.JPG")
    # print("haha")
    # print(f"{dst}{category}/*.JPG")
    # print("files")
    # print(files)
    # print(f"{Path(pattern).parent}/{category}/*.JPG")
    plot_multiple_images_histogram(files, src, dst,
                                    dst, category,
                                    augmented)

    return files


def process_input_transformation(src=None, dst=None, option=None, script=False) -> None:
    transformations = "lab", "hsv", "morphological_gradient", \
                      "bilateral_filter", "median_blur_small_noise", \
                      "canny_edge"
    # if src and not src.endswith('/'):
    #     src = src + '/'
    # if dst and not dst.endswith('/'):
    #     dst = src + '/'
    # elif not dst:
    #     dst = src
    # else:
    #     raise AssertionError("Please provide a path for files' transformation")
    img = None
    # print("SCRIPT")
    # print(f"{src}Transformed/*.JPG")
    pattern = f"{Path(src).parent}/{Path(src).name}" if script == False else f"{src}Base/*.JPG"
    ndst = f"{Path(pattern).parent.parent}/Transformed/"
    # print("lolo", f"{Path(src).parent}/{Path(src).name}")
    # print("destination", ndst)
    # print("NDSF")
    # print(ndst)
    print("NDSF")
    print(ndst)
    if src and path.isfile(src):
        # ndst = f"{path.normpath(path.dirname(src))}/Histogram_subcategory/"

        img = process_file(src, dst=ndst, category="Transformed",
                           augmented=False)
        # print("DSTTT")
        # print(ndst)
        get_lab(src, ndst)
        get_hsv(src, ndst)
        get_morphological_gradient(src, ndst)
        get_bilateral_filter(src, ndst)
        get_median_blurring_small_noise(src, ndst)
        get_canny_edge(src, ndst)
        image_paths = "_lab.JPG", "_hsv.JPG", "_morphological_gradient.JPG", "_bilateral_filter.JPG", "_median_blur_small_noise.JPG", "_canny_edge.JPG"
        complete_paths = []
        for ipath in image_paths:
            # print("patz")
            # print(pattern)
            filepath = Path(pattern).parent
            # filepath = f"{filepath}/Transformed"
            filename = Path(pattern).stem


            # Get full path without extension
            # result = full_path.with_suffix('')  # removes .JPG
            # print("LALALA")
            # print(f"{Path(pattern).parent.parent}/Transformed/")
            filepath = f"{Path(pattern).parent.parent}/Transformed/"
            complete_paths.append(f"{filepath}{filename}{ipath}")
        # print("complete paths")
        # print(complete_paths)
        n_images = 6
        n_cols = 3
        n_rows = 2

        fig_width_per_image = 3  # inches per image width
        fig_height_per_image = 4  # inches per image height

        fig, axes = subplots(n_rows, n_cols, figsize=(fig_width_per_image * n_cols, fig_height_per_image * n_rows))
        # Flatten axes array for easy iteration
        axes = axes.flatten()

        for i, ipath in enumerate(complete_paths):
            # print("ipath")
            # print(f"{ndst}{Path(ipath).name}")
            image = imread(f"{ndst}{Path(ipath).name}")
            # print("imgg")
            # print(f"{ndst}{Path(ipath).name}")
            axes[i].imshow(image)
        tight_layout()
        # output_path = src
        # savefig(output_path)
        show()

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

                get_lab(image, ndst)
                get_hsv(image, ndst)
                get_morphological_gradient(image, ndst)
                get_bilateral_filter(image, ndst)
                get_median_blurring_small_noise(image, ndst)
                get_canny_edge(image, ndst)
        else:
            print(f"No files found matching pattern: {pattern}")


if __name__ == "__main__":
    try:
        match get_len(argv):
            case 1:
                raise AssertionError("Error: Please provide at least \
                                      one argument.")
            case 2:
                process_input_transformation(src=argv[1])
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
