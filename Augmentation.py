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
from matplotlib.pyplot import savefig, close, subplots, tight_layout, show
from cv2 import imread, imshow, imwrite
from pathlib import Path

def process_input_augmentation(src=None, dst=None, script=False) -> None:
    augmentations = "contrast", "scale_zoom", "horizontal_flip", "rotation", \
                    "affine_transformation", "perspective_transformation"

    # if src and not src.endswith('/'):
    #     src = src + '/'
    # if dst and not dst.endswith('/'):
    #     dst = src + '/'
    # elif not dst:
    #     dst = src
    # else:
    #     raise AssertionError("Please provide a path for files' transformation")
    img = None
    # print("SRRRCCC")
    # print(Path(src).parent.parent)
    # destination = Path(src)
    # print("source")
    # print("pattern")
    # print(pattern)
    ndst = f"{src}Augmented/"
    # print(ndst)
    # print("SCRIPT")
    # print(f"{src}Transformed/*.JPG")
    pattern = f"{Path(src).parent}/{Path(src).name}" if script == False else f"{src}Transformed/*.JPG"
    # print("patt")
    # print(pattern)
    # print(src)
    # print("NDSF")
    # print(ndst)
    # print(f"{Path(pattern).parent.parent}/Augmented/")

    if src and path.isfile(src):
        img = process_file(src, dst=ndst, category="Augmented",
                           augmented=True)
        # print("DSTTT")
        print('sourcz')
        print(src)
        get_contrast(src, ndst)
        get_scale_zoom(src, ndst)
        get_horizontal_flip(src, ndst)
        get_rotate(src, ndst)
        get_affine_transformation(src, ndst)
        get_perspective_transformation(src, ndst)
        image_paths = "_contrast.JPG", "_scale_zoom.JPG", "_horizontal_flip.JPG", "_rotation.JPG", "_affine_transformation.JPG", "_perspective_transformation.JPG"
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
            # print(f"{Path(pattern).parent.parent}/Augmented/")
            filepath = f"{Path(pattern).parent.parent}/Augmented/"
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
        # Try to find multiple files using glob pattern
        # Pattern for images starting with prefix
        img = glob(pattern)

        if img:
            print(f"Found {get_len(img)} files matching pattern: {pattern}")
            # plot_multiple_images_histogram(img, src, ndst)
            for i, image in enumerate(img):
                if script:
                    process_file(image, dst=dst, category="Transformed",
                             augmented=True)
                get_contrast(image, ndst)
                get_scale_zoom(image, ndst)
                get_horizontal_flip(image, ndst)
                get_rotate(image, ndst)
                get_affine_transformation(image, ndst)
                get_perspective_transformation(image, ndst)
        else:
            print(f"No files found matching pattern: {pattern}")


if __name__ == "__main__":
    # print(len(argv))
    try:
        
        match get_len(argv):
            case 1:
                raise AssertionError("Error: Please provide at least one \
                                      argument.")
            case 2:
                process_input_augmentation(src=argv[1])
            case 3:
                if argv[2] == "--script":
                    process_input_augmentation(src=f"{argv[1]}/", script=True)
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
