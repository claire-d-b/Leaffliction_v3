#!/usr/bin/env python3

from cv2 import (imread, imwrite, resize, INTER_AREA, INTER_CUBIC,
                 getRotationMatrix2D, warpAffine, convertScaleAbs,
                 flip, getAffineTransform, getPerspectiveTransform,
                 warpPerspective)
from numpy import float32
from os import path


def get_contrast(src: str, dst: str, script=False):

    # subdir = "Augmented"
    filename = path.splitext(path.basename(src))[0]

    # CONTRAST / BRIGHTNESS
    img = imread(src)
    alpha = 2.0
    # 1-3
    beta = 50
    # 0-100
    img_contrast = convertScaleAbs(img, alpha=alpha, beta=beta)
    # print("CONTRAST")
    # print(f"{dst}/{filename}_contrast.JPG")
    # print("contrast")
    # print(f"{dst}/{filename}_contrast.JPG")
    imwrite(f"{dst}/{filename}_contrast.JPG", img_contrast)
    # but we wanted to show you how to access the pixels:

    # for y in range(image.shape[0]):
    #     for x in range(image.shape[1]):
    #         for c in range(image.shape[2]):
    #             new_image[y,x,c] = clip(alpha*image[y,x,c] + beta, 0, 255)


def get_scale_shrink(src: str, dst: str, script=False):
    # SCALE
    # subdir = "Augmented"
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    height, width = img.shape[:2]
    img_shrinked = resize(img, (width//4, height//4), interpolation=INTER_AREA)
    imwrite(f"{dst}/{filename}_shrink.JPG", img_shrinked)


def get_scale_zoom(src: str, dst: str, script=False):
    # subdir = "Augmented"
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    height, width = img.shape[:2]
    img_zoomed = resize(img, (width*2, height*2), interpolation=INTER_CUBIC)
    imwrite(f"{dst}/{filename}_scale_zoom.JPG", img_zoomed)

# def get_scale_zoom_crop(src: str, dst: str, script=False):
    subdir = "Augmented"
#     filename = path.splitext(path.basename(src))[0]
#     img = imread(src)
#     height, width = img.shape[:2]
#     img_zoomed = resize(img,(width*2, height*2), interpolation=INTER_CUBIC)
#     y, x = img_zoomed.shape[:2]  # Get image height and width
#     cropx = x//3
#     cropy = y//3
#     startx = x//2 - cropx//2
#     starty = y//2 - cropy//2
#     img_zoomed_cropped = img_zoomed[starty:starty+cropy, startx:startx+cropx]
#     imwrite(f"{dst}/{filename}_zoomed_cropped.JPG",
#     img_zoomed_cropped)


def get_horizontal_flip(src: str, dst: str, script=False):
    # subdir = "Augmented"
    # FLIP
    # Different flip operations
    # flipCode = 0: Vertical flip (top-bottom)
    # vertical_flip = cv2.flip(img, 0)
    # vertical_flip_rgb = cv2.cvtColor(vertical_flip, cv2.COLOR_BGR2RGB)

    # flipCode = 1: Horizontal flip (left-right)
    # horizontal_flip = cv2.flip(img, 1)
    # horizontal_flip_rgb = cv2.cvtColor(horizontal_flip, cv2.COLOR_BGR2RGB)

    # flipCode = -1: Both horizontal and vertical flip
    # both_flip = cv2.flip(img, -1)
    # both_flip_rgb = cv2.cvtColor(both_flip, cv2.COLOR_BGR2RGB)
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    img_horizontal_flip = flip(img, 1)
    imwrite(f"{dst}/{filename}_horizontal_flip.JPG",
            img_horizontal_flip)


def get_rotate(src: str, dst: str, script=False):
    # subdir = "Augmented"
    # ROTATE
    # getRotationMatrix2D Params:
    # center: Center of the rotation in the source image.
    # angle: Rotation angle in degrees. Positive values mean
    # counter-clockwise rotation (the coordinate origin is
    # assumed to be the top-left corner).
    # scale: Isotropic scale factor.
    # warpAffine Params:
    # src: input image.
    # dst: output image that has the size dsize and the same type as src .
    # M: transformation matrix.
    # dsize: size of the output image.
    # flags: combination of interpolation methods (see InterpolationFlags)
    # and the optional flag WARP_INVERSE_MAP (that means that M is
    # the inverse transformation).
    # borderMode: pixel extrapolation method (see BorderTypes);
    # when borderMode=BORDER_TRANSPARENT, it means that the pixels in
    # the destination image corresponding to the "outliers" in the
    # source image are not modified by the function.
    # borderValue: value used in case of a constant border;
    # by default, it is 0.
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    height, width = img.shape[:2]
    rotated = getRotationMatrix2D(((height-1)/2.0, (width-1)/2.0), 90, 1)
    img_rotated = warpAffine(img, rotated, (height, width))
    imwrite(f"{dst}/{filename}_rotation.JPG", img_rotated)


def get_affine_transformation(src: str, dst: str, script=False) -> None:
    # subdir = "Augmented"
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    rows, cols, ch = img.shape

    pts1 = float32([[50, 50], [200, 50], [50, 200]])
    pts2 = float32([[10, 100], [200, 50], [100, 250]])

    M = getAffineTransform(pts1, pts2)

    image = warpAffine(img, M, (cols, rows))
    imwrite(f"{dst}/{filename}_affine_transformation.JPG", image)


def get_perspective_transformation(src: str, dst: str, script=False) -> None:
    # subdir = "Augmented"
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    rows, cols, ch = img.shape

    # HG,HD,BD,BG
    pts1 = float32([[cols*1/12, rows*1/12], [cols*11/12, rows*1/12],
                    [cols*11/12, rows*11/12], [cols*1/12, rows*11/12]])

    # OPTION 1: Taille fixe (recommandée)
    # Points destination - taille raisonnable
    output_width = cols  # ou une valeur fixe comme 800
    output_height = rows  # ou une valeur fixe comme 600

    pts2 = float32([
        [0, 0],
        [output_width, 0],
        [output_width, output_height],
        [0, output_height]
    ])

    M = getPerspectiveTransform(pts1, pts2)
    image = warpPerspective(img, M, (output_width, output_height))
    imwrite(f"{dst}/{filename}_perspective_transformation.JPG", image)
