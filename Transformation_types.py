#!/usr/bin/env python3

from cv2 import (imread, imwrite, cvtColor, COLOR_BGR2HLS, COLOR_BGR2HSV, COLOR_BGR2YUV, COLOR_BGR2GRAY,
                 medianBlur, getGaussianKernel, GaussianBlur, bilateralFilter,
                 BORDER_CONSTANT, morphologyEx, MORPH_ELLIPSE, MORPH_GRADIENT, getStructuringElement, BORDER_DEFAULT, Sobel, CV_16S, convertScaleAbs, addWeighted, COLOR_BGR2GRAY, Laplacian, blur, Canny, COLOR_BGR2LAB)
from numpy import exp, ones, uint8
from os import path


# rgb_image = cvtColor(img, COLOR_BGR2RGB)
# Get RGB values at specific pixel (x, y)
# x, y = 10, 10 # pixel coordinates - background
# x, y = width // 2, height // 2 # pixel coordinates - leaf
# rgb_values = rgb_image[y, x]  # Note: [row, column] = [y, x]
# print(f"RGB values at ({x}, {y}): R={rgb_values[0]},
# G={rgb_values[1]}, B={rgb_values[2]}")
# we notice that R value is upper than others


def get_hls(src: str, dst: str) -> None:
    subdir = "Transformed"
    # hue lightness saturation
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    img_color_hls = cvtColor(img, COLOR_BGR2HLS)
    imwrite(f"{dst}/{subdir}/{filename}_hls.JPG", img_color_hls)


def get_lab(src: str, dst: str) -> None:
    subdir = "Transformed"
    # hue lightness saturation
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    img_color_lab = cvtColor(img, COLOR_BGR2LAB)
    imwrite(f"{dst}/{subdir}/{filename}_lab.JPG", img_color_lab)

def get_yuv(src: str, dst: str) -> None:
    subdir = "Transformed"
    # hue lightness saturation
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    img_color_yuv = cvtColor(img, COLOR_BGR2YUV)
    imwrite(f"{dst}/{subdir}/{filename}_yuv.JPG", img_color_yuv)

def get_gray(src: str, dst: str) -> None:
    subdir = "Transformed"
    # hue lightness saturation
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    img_color_gray = cvtColor(img, COLOR_BGR2GRAY)
    imwrite(f"{dst}/{subdir}/{filename}_gray.JPG", img_color_gray)

def get_hsv(src: str, dst: str) -> None:
    # hue saturation value
    # print("dst")
    # print(dst)
    subdir = "Transformed"
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    img_color_hsv = cvtColor(img, COLOR_BGR2HSV)
    imwrite(f"{dst}/{subdir}/{filename}_hsv.JPG", img_color_hsv)


def get_gaussian_blur(src: str, dst: str) -> None:
    # GAUSSIAN BLURRING
    subdir = "Transformed"
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)

    kernel_size = 5
    ksize = (5, 5)

    kernel = getGaussianKernel(kernel_size, kernel_size/2 * exp(-0.5))
    center = kernel_size // 2
    # Find positions where kernel drops to ~60.65% of center value
    # (this corresponds to 1 standard deviation)
    center_value = kernel[center]
    target_value = center_value * exp(-0.5)  # e^(-0.5) ≈ 0.6065

    # Find the position closest to this target
    distances = []
    for i in range(center + 1, kernel_size):
        if kernel[i] <= target_value:
            sigma_estimate = i - center
            distances.append(sigma_estimate)
            break

    sigma = distances[0]
    # sigmaX and sigmaY of 0 = calculated from the kernel size
    img_gaussian_blur = GaussianBlur(img, ksize, sigma)

    imwrite(f"{dst}/{subdir}/{filename}_gaussian_blur.JPG", img_gaussian_blur)
    # GaussianBlur Params:
    # src: input image; the image can have any number of channels,
    # which are processed independently,
    # but the depth should be CV_8U, CV_16U, CV_16S, CV_32F or CV_64F.
    # dst: output image of the same size and type as src.
    # ksize: Gaussian kernel size. ksize.width and ksize.height can
    # differ but they both must be positive and odd. Or, they can be
    # zero's and then they are computed from sigma.
    # sigmaX: Gaussian kernel standard deviation in X direction.
    # sigmaY: Gaussian kernel standard deviation in Y direction;
    # if sigmaY is zero, it is set to be equal to sigmaX, if both sigmas
    # are zeros, they are computed from ksize.width and ksize.height,
    # respectively (see getGaussianKernel for details); to fully control
    # the result regardless of possible future modifications of all
    # this semantics, it is recommended to specify all of ksize,
    # sigmaX, and sigmaY.
    # borderType: pixel extrapolation method, see BorderTypes.
    # BORDER_WRAP is not supported.
    # hint: Implementation modfication flags. See AlgorithmHint

    # getGaussianKernel: Returns Gaussian filter coefficients.
    # The function computes and returns the matrix of Gaussian
    # filter coefficients:
    # Parameters:
    # ksize: Aperture size. It should be odd (and positive).
    # sigma: Gaussian standard deviation. If it is non-positive, it is computed
    # from ksize as sigma = 0.3*((ksize-1)*0.5 - 1) + 0.8.
    # ktype: Type of filter coefficients. It can be CV_32F or CV_64F.


def get_bilateral_filter(src: str, dst: str) -> None:
    # BILATERAL FILTER
    # src: Source 8-bit or floating-point, 1-channel or 3-channel image.
    # dst: Destination image of the same size and type as src.
    # d: Diameter of each pixel neighborhood that is used during filtering.
    # If it is non-positive, it is computed from sigmaSpace.
    # sigmaColor: Filter sigma in the color space. A larger value of the
    # parameter means that farther colors within the pixel neighborhood
    # (see sigmaSpace) will be mixed together, resulting in larger
    # areas of semi-equal color.
    # sigmaSpace: Filter sigma in the coordinate space. A larger value
    # of the parameter means that farther pixels will influence each other
    # as long as their colors are close enough (see sigmaColor).
    # When d>0, it specifies the neighborhood size regardless of sigmaSpace.
    # Otherwise, d is proportional to sigmaSpace.
    # borderType: border mode used to extrapolate pixels outside of the
    # image, see BorderTypes
    # Low sigmaColor (e.g., 10-30):
    # Only very similar colors get averaged together
    # Preserves edges strongly
    # Less smoothing overall
    # Sharp color transitions remain sharp
    # High sigmaColor (e.g., 80-150):
    # Allows more different colors to be averaged
    # More aggressive smoothing
    # Edges become softer
    # Different colors blend more
    # Low sigmaSpace (e.g., 10-30):
    # Only considers nearby pixels
    # Faster processing
    # More localized smoothing
    # Fine details preserved
    # High sigmaSpace (e.g., 80-150):
    # Considers pixels farther away
    # Slower processing
    # Broader smoothing effect
    # Can smooth larger areas
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)

    nimg = None
    img_bilateral_filter = bilateralFilter(img, nimg,
                                           sigmaColor=5*20, sigmaSpace=5*20,
                                           borderType=BORDER_CONSTANT)
    subdir = "Transformed"

    imwrite(f"{dst}/{subdir}/{filename}_bilateral_filter.JPG",
            img_bilateral_filter)
    # Used for denoising!
    # See, the texture on the surface is gone, but the edges are
    # still preserved.


def get_median_blurring_small_noise(src: str, dst: str) -> None:
    # MEDIAN BLURRING
    # cv.medianBlur(	src, ksize[, dst]	) -> 	dst
    # src: input 1-, 3-, or 4-channel image;
    # when ksize is 3 or 5, the image depth should be CV_8U, CV_16U, or CV_32F,
    # for larger aperture sizes, it can only be CV_8U.
    # dst: destination array of the same size and type as src.
    # ksize: aperture linear size; it must be odd and greater than 1,
    # for example: 3, 5, 7 ...
    # Aperture: The size of the kernel or neighborhood used in various
    # image processing operations.
    # 3 vs 5 - 3 looks at broader neighborhood, remove larger noise patterns
    # Removes salt and pepper effect - small noise
    subdir = "Transformed"
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    img_median_blur_small = medianBlur(img, 3)
    imwrite(f"{dst}/{subdir}/{filename}_median_blur_small_noise.JPG",
            img_median_blur_small)


def get_median_blurring_large_noise(src: str, dst: str) -> None:
    # Remove salt and paper effect - large noise
    subdir = "Transformed"
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    img_median_blur_large = medianBlur(img, 5)
    imwrite(f"{dst}/{subdir}/{filename}_median_blur_large_noise.JPG",
            img_median_blur_large)

def get_morphological_gradient(src: str, dst: str) -> None:
    subdir = "Transformed"
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    
    kernel = ones((3, 3), uint8)
    img_morphological_gradient = morphologyEx(img, MORPH_GRADIENT, kernel)
        
    imwrite(f"{dst}/{subdir}/{filename}_morphological_gradient.JPG",
            img_morphological_gradient)

def get_sobel(src: str, dst: str) -> None:
    subdir = "Transformed"
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)
    scale = 1
    delta = 0
    ddepth = CV_16S

    gray = cvtColor(img, COLOR_BGR2GRAY)

    grad_x = Sobel(gray, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=BORDER_DEFAULT)
    # Gradient-Y
    # grad_y = Scharr(gray,ddepth,0,1)
    grad_y = Sobel(gray, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=BORDER_DEFAULT)
    
    
    abs_grad_x = convertScaleAbs(grad_x)
    abs_grad_y = convertScaleAbs(grad_y)
    
    
    img_sobel = addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    imwrite(f"{dst}/{subdir}/{filename}_sobel.JPG",
            img_sobel)

def get_laplacian_operator(src: str, dst: str) -> None:
    subdir = "Transformed"
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)

    ddepth = CV_16S
    kernel_size = 3
    src = GaussianBlur(img, (3, 3), 0)
    # [reduce_noise]
    # [convert_to_gray]
    # Convert the image to grayscale
    src_gray = cvtColor(img, COLOR_BGR2GRAY)
    img_laplacian = Laplacian(src_gray, ddepth, ksize=kernel_size)
    # Convert CV_16S to CV_8U for saving
    img_laplacian_operator_8u = convertScaleAbs(img_laplacian)
    imwrite(f"{dst}/{subdir}/{filename}_laplacian_operator.JPG",
            img_laplacian_operator_8u)

def get_canny_edge(src: str, dst: str) -> None:
    subdir = "Transformed"
    filename = path.splitext(path.basename(src))[0]
    img = imread(src)

    low_threshold = 0
    ratio = 3
    kernel_size = 3

    img_blur = blur(img, (3,3))
    detected_edges = Canny(img_blur, low_threshold, low_threshold*ratio, kernel_size)
    mask = detected_edges != 0
    img_canny_edge = img * (mask[:,:,None].astype(img.dtype))
    imwrite(f"{dst}/{subdir}/{filename}_canny_edge.JPG",
            img_canny_edge)