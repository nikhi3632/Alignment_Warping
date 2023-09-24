from align_channels import align_channels
import numpy as np
import os
import shutil

# Image Alignment
def main(DATA_DIR, RESULT_DIR, args):
    # 1. Load images (all 3 channels)

    # 2. Find best channels alignment

    # 3. save result to rgb_output.jpg (IN THE "results" FOLDER)
    pass

if __name__ == "__main__":
    DATA_DIRECTORY = "data/"
    RESULTS_DIRECTORY = "align_results/"
    if os.path.exists(RESULTS_DIRECTORY):
        shutil.rmtree(os.path.join(os.getcwd(), RESULTS_DIRECTORY))
    os.mkdir(RESULTS_DIRECTORY)
    main(DATA_DIRECTORY, RESULTS_DIRECTORY)
