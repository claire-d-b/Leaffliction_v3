#!/usr/bin/env python3

from sys import argv
from glob import glob
from os import path
from Augmentation_types import (get_contrast, get_scale_zoom,
                                get_horizontal_flip, get_rotate,
                                get_perspective_transformation,
                                get_affine_transformation)
from Transformation import process_file
from stats import get_len


def process_input_augmentation(src=None, dst=None, option=None) -> None:
    augmentations = "contrast", "scale_zoom", "horizontal_flip", "rotation", \
                    "affine_transformation", "perspective_transformation"

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
                           augmented=True)
        if option:
            for i, ttype in enumerate(augmentations):
                match option:
                    case 0:
                        return get_contrast(src, dst)
                    case 1:
                        return get_scale_zoom(src, dst)
                    case 2:
                        return get_horizontal_flip(src, dst)
                    case 3:
                        return get_rotate(src, dst)
                    case 4:
                        return get_affine_transformation(src, dst)
                    case 5:
                        return get_perspective_transformation(src, dst)
                    case _:
                        return None

        else:
            get_contrast(src, dst)
            get_scale_zoom(src, dst)
            get_horizontal_flip(src, dst)
            get_rotate(src, dst)
            get_affine_transformation(src, dst)
            get_perspective_transformation(src, dst)

    else:
        folder = src
        # Try to find multiple files using glob pattern
        # Pattern for images starting with prefix
        pattern = f"{folder}Transformed/*.JPG"
        img = glob(pattern)

        ndst = f"{folder}Histogram_subcategory/"
        if img:
            print(f"Found {get_len(img)} files matching pattern: {pattern}")
            # plot_multiple_images_histogram(img, src, ndst)
            for i, image in enumerate(img):
                process_file(image, dst=dst, category="Transformed",
                             augmented=True)

                if option:
                    for i, ttype in enumerate(augmentations):
                        match option:
                            case 0:
                                return get_contrast(image, dst)
                            case 1:
                                return get_scale_zoom(image, dst)
                            case 2:
                                return get_horizontal_flip(image, dst)
                            case 3:
                                return get_rotate(image, dst)
                            case 4:
                                return get_affine_transformation(image, dst)
                            case 5:
                                return get_perspective_transformation(image,
                                                                      dst)
                            case _:
                                return None
                else:
                    get_contrast(image, dst)
                    get_scale_zoom(image, dst)
                    get_horizontal_flip(image, dst)
                    get_rotate(image, dst)
                    get_affine_transformation(image, dst)
                    get_perspective_transformation(image, dst)
        else:
            print(f"No files found matching pattern: {src}")


if __name__ == "__main__":
    try:
        match get_len(argv):
            case 1:
                raise AssertionError("Error: Please provide at least one \
                                      argument.")
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
                    raise AssertionError("Error: Unknown commmand: see \
                                          Augmentation.py -h (help).")
            case 7:
                if argv[1] == '-src' and argv[3] == '-dst' and argv[5] == \
                   '-options':
                    process_input_augmentation(src=argv[2], dst=argv[4],
                                               option=argv[6])
            case _:
                raise AssertionError("Error: Too many arguments.")

    except AssertionError as error:
        print(f"{error}")
