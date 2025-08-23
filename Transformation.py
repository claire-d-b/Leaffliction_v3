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

    if not augmented:
        files = glob(f"{Path(pattern).parent}/Transformed/*.JPG")
        # print("files")
        # print(files)
        print(f"{Path(pattern).parent}/Transformed/*.JPG")
        plot_multiple_images_histogram(files, src, dst,
                                       ndst, category,
                                       augmented)
        return files
    else:
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


def process_input_augmentation(src=None, dst=None, option=None) -> None:
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
    if src and path.isfile(src):
        ndst = f"{path.normpath(path.dirname(src))}/Histogram_subcategory/"

        img = process_file(src, dst=ndst, category="Transformed",
                           augmented=False)
        if option:
            for i, ttype in enumerate(transformations):
                match option:
                    case 0:
                        return get_hls(src, dst)
                    case 1:
                        return get_hsv(src, dst)
                    case 2:
                        return get_gaussian_blur(src, dst)
                    case 3:
                        return get_bilateral_filter(src, dst)
                    case 4:
                        return get_median_blurring_small_noise(src, dst)
                    case 5:
                        return get_median_blurring_large_noise(src, dst)
                    case _:
                        return None
        else:
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
        pattern = f"{folder}Base/*.JPG"
        img = glob(pattern)

        ndst = f"{folder}Histogram_subcategory/"
        if img:
            print(f"Found {get_len(img)} files matching pattern: {pattern}")
            # plot_multiple_images_histogram(img, src, ndst)
            for i, image in enumerate(img):
                process_file(image, dst=dst, category="Transformed",
                             augmented=False)

                if option:
                    for i, ttype in enumerate(transformations):
                        match option:
                            case 0:
                                return get_morphological_gradient(image, dst)
                            case 1:
                                return get_sobel(image, dst)
                            case 2:
                                return get_canny_edge(image, dst)
                            case 3:
                                return get_median_blurring_large_noise(image,
                                                                       dst)
                            case 4:
                                return get_median_blurring_small_noise(
                                       image, dst)
                            case 5:
                                return get_laplacian_operator(image, dst)
                            case _:
                                return None
                else:
                    get_lab(image, dst)
                    get_hsv(image, dst)
                    get_morphological_gradient(image, dst)
                    get_bilateral_filter(image, dst)
                    get_median_blurring_small_noise(image, dst)
                    get_canny_edge(image, dst)
        else:
            print(f"No files found matching pattern: {src}")


if __name__ == "__main__":
    try:
        match get_len(argv):
            case 1:
                raise AssertionError("Error: Please provide at least \
                                      one argument.")
            case 2 | 3:
                if get_len(argv) == 2 and argv[1] == "-h":
                    print("usage: Augmentation.py [-h] [-src] \
                           [-dst] [options]\noptional arguments:\n\
                           -h, --help  show this help message and \
                           exit\n -src <Input directory>\n -dst \
                           <Destination directory if multiple files>\n\
                           -options Type of Augmentation\n\
                           <hls> Convert image to hue-lightness-saturation\n\
                           <hsv> Convert image to hue-saturation-value\n\
                                <gaussian-blur> It softens the edges and \
                            reduces high-frequency noise in the image \
                            by averaging pixel values\n\
                                <median-blur-small> Removes 'salt and \
                            pepper' small noise\n\
                                <median-blur-large> \
                            Removes 'salt and pepper' large noise\n\
                                <bilateral-filter> Removes noise and \
                            preserves edges")
                elif get_len(argv) == 2:
                    process_input_augmentation(src=argv[1])
                else:
                    if argv[1] == '-src':
                        process_input_augmentation(src=argv[2])
            case 5:
                if argv[1] == '-src' and argv[3] == '-dst':
                    process_input_augmentation(src=argv[2], dst=argv[4])
                else:
                    raise AssertionError("Error: Unknown commmand: \
                                          see Augmentation.py -h (help).")
            case 7:
                if argv[1] == '-src' and argv[3] == '-dst' and \
                   argv[5] == '-options':
                    process_input_augmentation(src=argv[2],
                                               dst=argv[4], option=argv[6])
            case _:
                raise AssertionError("Error: Too many arguments.")

    except AssertionError as error:
        print(f"{error}")
