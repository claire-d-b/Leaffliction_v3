#!/usr/bin/env python3

from cv2 import (imread, cvtColor, COLOR_BGR2HLS, COLOR_BGR2HSV, calcHist,
                 split, COLOR_BGR2LAB)
from matplotlib.pyplot import (legend, close, title, xlabel, ylabel, savefig,
                               ylim, subplots)
from pathlib import Path
from numpy import ndarray
from os import path
from pandas import DataFrame, concat, read_csv
from utils import load
from stats import (get_len, get_min, get_max, get_standard_deviation,
                   get_quartile, get_median, get_mean)
from sys import argv
import glob


# Helper to calculate histogram
def calc_hist(channel):
    return calcHist([channel], [0], None, [256], [0, 256])


def get_additional_values(img: ndarray) -> tuple:
    # Tuple is an immutable ordered collection of items.
    # Convert to HLS and HSV color spaces
    hls_img = cvtColor(img, COLOR_BGR2HLS)
    hsv_img = cvtColor(img, COLOR_BGR2HSV)

    # Split channels
    h_hls, l, s_hls = split(hls_img)  # HLS channels
    h_hsv, s_hsv, v = split(hsv_img)  # HSV channels

    return (l, h_hls, s_hls, v)


def calculate_histogram_stats(values):
    """Calculate statistics from histogram data"""
    return get_len(values), get_mean(values), get_standard_deviation(values),
    get_min(values), get_quartile(values)[0], get_median(values),
    get_quartile(values)[1], get_max(values)


def plot_multiple_images_histogram(image_files, src, dst, ndst, category,
                                   augmented):
    """Plot averaged histograms for multiple images"""
    fig, axs = subplots()

    # Initialize histogram accumulators
    (r_hist_sum, g_hist_sum, b_hist_sum, l_hist_sum, h_hist_sum, s_hist_sum,
     v_hist_sum) = None, None, None, None, None, None, None

    valid_images = 0

    for file in image_files:
        img = imread(file)

        if img is None:
            # print(f"Warning: Could not read image {file} because \
            #        of incorrect format (.csv)")
            continue
        else:
            valid_images += 1

        height, width = img.shape[:2]
        total_pixels = width * height

        # Split BGR channels
        b, g, r = split(img)

        # Convert to LAB color space
        lab_img = cvtColor(img, COLOR_BGR2LAB)
        # Ligthness + blue-yellow and green-magenta
        # = colors that cancel each other
        L, A, B = split(lab_img)

        # A channel = Green-Magenta axis
        # B channel = Blue-Yellow axis

        # Get additional color space channels
        l, h_hls, s_hls, v = get_additional_values(img)

        # Calculate histograms and normalize
        r_hist = calc_hist(r) / total_pixels * 100
        g_hist = calc_hist(g) / total_pixels * 100
        b_hist = calc_hist(b) / total_pixels * 100

        A_hist = calc_hist(A) / total_pixels * 100
        B_hist = calc_hist(B) / total_pixels * 100

        l_hist = calc_hist(l) / total_pixels * 100
        h_hist = calc_hist(h_hls) / total_pixels * 100
        s_hist = calc_hist(s_hls) / total_pixels * 100
        v_hist = calc_hist(v) / total_pixels * 100

        # Accumulate histograms
        if r_hist_sum is None:
            r_hist_sum = r_hist
            g_hist_sum = g_hist
            b_hist_sum = b_hist
            A_hist_sum = A_hist
            B_hist_sum = B_hist
            l_hist_sum = l_hist
            h_hist_sum = h_hist
            s_hist_sum = s_hist
            v_hist_sum = v_hist
        else:
            r_hist_sum += r_hist
            g_hist_sum += g_hist
            b_hist_sum += b_hist
            A_hist_sum += A_hist
            B_hist_sum += B_hist
            l_hist_sum += l_hist
            h_hist_sum += h_hist
            s_hist_sum += s_hist
            v_hist_sum += v_hist

    if valid_images == 0:
        return

    # Average the histograms
    r_hist_avg = r_hist_sum / valid_images
    g_hist_avg = g_hist_sum / valid_images
    b_hist_avg = b_hist_sum / valid_images

    A_hist_avg = A_hist_sum / valid_images
    B_hist_avg = B_hist_sum / valid_images

    l_hist_avg = l_hist_sum / valid_images
    h_hist_avg = h_hist_sum / valid_images
    s_hist_avg = s_hist_sum / valid_images
    v_hist_avg = v_hist_sum / valid_images

    if category == "Transformed" or category == "Augmented":
        nsrc = path.basename(src)
        dst = f"{dst}{category}/"

        modifications = ("lab", "hsv", "morphological_gradient",
                         "bilateral_filter", "median_blur_small_noise",
                         "canny_edge") if not augmented else \
                        ("contrast", "scale_zoom",
                         "horizontal_flip", "rotation",
                         "affine_transformation",
                         "perspective_transformation")

        for m in modifications:
            dstname = f"{dst}{path.splitext(path.basename(nsrc))[0]}_{m}"
            dictionary = dict({
                            "Subname": f"{Path(dstname).name.split('_')[0]}_\
{Path(dstname).parts[1]}",
                            "Name": f"{Path(dstname).name.split('_')[0]}_\
{Path(dstname).parts[1]}_{'_'.join(Path(dstname).name.split('_')[1:])}",
                            "Category": f"{Path(dstname).parts[1]}",
                            "Modification": f"{'_'.join(Path(dstname)
                                                        .name.split('_')
                                                        [1:])}",
                            "Red": r_hist_avg.flatten(),
                            "Green": g_hist_avg.flatten(),
                            "Blue": b_hist_avg.flatten(),
                            "Blue_Yellow": A_hist_avg.flatten(),
                            "Green_Magenta": B_hist_avg.flatten(),
                            "Lightness": l_hist_avg.flatten(),
                            "Hue": h_hist_avg.flatten(),
                            "Saturation": s_hist_avg.flatten(),
                            "Value": v_hist_avg.flatten()})
            ndf = DataFrame(dictionary)
            # ndf = normalize_df(ndf)

            ndst = Path(dst).parent
            # print("first path")
            # print(f'{Path(dst).parent}/{Path(dstname).parts[1]}_features.csv')
            # print("second path")
            # print(f"{Path(dst).parent}/{Path(dstname).parts[1]}_features.csv")
            if path.exists(f'{Path(dst).parent}/{Path(dstname).parts[1]}_features.csv'):
                ndf.to_csv(f'{Path(dst).parent}/{Path(dstname).parts[1]}_features.csv', mode='a', header=False)
            else:
                ndf.to_csv(f'{Path(dst).parent}/{Path(dstname).parts[1]}_features.csv', mode='w', index=True)

            newdf = load(f"{Path(dst).parent}/{Path(dstname).parts[1]}_features.csv")
            nndf = newdf.groupby(['Subname', 'Name', 'Category',
                                  'Modification']).sum(numeric_only=True)
            nndf = normalize_df(nndf)
            # nndf = normalize_df(nndf)
            # print("whhhhhhat ?")
            # print(f"{Path(dst).parent}/{argv[1].rsplit('/', 1)[1]}_features_test.csv")
            nndf.to_csv(f"{Path(dst).parent}/{argv[1].rsplit('/', 1)[1]}_features_test.csv", mode='w')
        # print("patternnnn")
        # print(f"**/*{Path(dst).parent}/{argv[1].rsplit('/', 1)[1]}_features_test.csv")
        pattern = f"**/*{Path(dst).parent}/{argv[1].rsplit('/', 1)[1]}_features_test.csv"
        # print("PATTERN")
        # print(pattern)
        csv_files = glob.glob(pattern, recursive=True)
        # print(files)
        # print("arg")
        # print(argv[1])
        # print(f"./*/*/*_{argv[1]}_features_test.csv")
        # csv_files = list(Path("./").glob(f"*_{argv[1]}_features_test.csv"))

        # Combine files
        # Combine files with only one header
        dfs = []
        for i, file in enumerate(csv_files):
            # print(file)

            if i == 0:
                # First file: keep header
                df = read_csv(file)
            else:
                # Subsequent files: skip header (first row)
                df = read_csv(file, skiprows=1, header=None)
                # Use column names from the first dataframe
                df.columns = dfs[0].columns

            dfs.append(df)
        # print("DFS")
        # print(dfs)
        combined_df = concat(dfs, ignore_index=True)
        # original_df = read_csv(csv_files[0])  # Get column structure
        # from first file
        # Get 2nd column name:
        # second_column_name = original_df.columns[1]
        test_df = combined_df.copy()
        # test_df = normalize_df(test_df)
        file = Path(f"{Path(dstname).parts[1]}")

        if file.exists():
            test_df.to_csv(f"features_{Path(dstname).parts[1]}\
.csv", mode="a", header=False)
            # test_df['Category'] = None
            test_df.to_csv(f"features_{Path(dstname).parts[1]}_test\
.csv", mode="a", header=False, index=False)
        else:
            test_df.to_csv(f"features_{Path(dstname).parts[1]}\
.csv", mode="w", header=True)
            # test_df['Category'] = None
            test_df.to_csv(f"features_{Path(dstname).parts[1]}\
.csv", mode="w", header=True, index=False)
        # Insert empty 2nd column back into the combined dataframe
        # Insert at position 1 with None values
        # combined_df.insert(1, second_column_name, None)
        # test_df.to_csv("features_test.csv", mode="a", index=False)

    # Plot averaged histograms
    axs.plot(b_hist_avg, color='b', label='Blue')
    axs.plot(A_hist_avg, color='yellow', label='Blue-Yellow')
    axs.plot(g_hist_avg, color='g', label='Green')
    axs.plot(B_hist_avg, color='fuchsia', label='Green-magenta')
    axs.plot(h_hist_avg, color='purple', label='Hue')
    axs.plot(l_hist_avg, color='gray', label='Lightness')
    axs.plot(r_hist_avg, color='r', label='Red')
    axs.plot(s_hist_avg, color='cyan', label='Saturation')
    axs.plot(v_hist_avg, color='orange', label='Value')

    title(f'Average Color Histogram - {valid_images} Images')
    xlabel('Pixel Intensity')
    ylabel('Average Proportion of pixels')
    ylim(0, 10)

    handles, labels = axs.get_legend_handles_labels()
    unique = dict(zip(labels, handles))
    legend(unique.values(), unique.keys())

    # source = path.splitext(path.basename(src))[0]
    output_path = f"{ndst}_color_histogram_multiple.png"
    savefig(output_path)

    axs.clear()
    fig.clf()
    close(fig)
