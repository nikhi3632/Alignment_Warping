import imageio
import os
import shutil
import matplotlib.pyplot as plt
import numpy as np
import warp_inbuilt
import warp

def main(INPUT_IMG, OUTPUT_IMG):
    # Read the image
    im = imageio.v2.imread(INPUT_IMG)
    im = im / 255.0  # convert to float

    # convert to grayscale
    im_gray = np.dot(im, [0.299, 0.587, 0.114])

    # create figure
    f, axes = plt.subplots(2, 2)
    f.set_size_inches(8, 8)
    axes[0, 0].imshow(im)
    axes[0, 0].set_title('original')
    axes[0, 1].imshow(im_gray, cmap=plt.get_cmap('gray'))
    axes[0, 1].set_title('grayscale')

    # define some helper functions
    # to create affine transformations
    def scalef(s):
        return np.diag([s, s, 1])


    def transf(tx, ty):
        A = np.eye(3)
        A[0, 2] = ty
        A[1, 2] = tx
        return A


    def rotf(t):
        return np.array([
                        [np.cos(t), np.sin(t), 0],
                        [-np.sin(t), np.cos(t), 0],
                        [0, 0, 1]
                        ])

    output_shape = im_gray.shape
    cx = im_gray.shape[1] // 2
    cy = im_gray.shape[0] // 2

    A = (transf(output_shape[1]//2, output_shape[0]//2,)
        .dot(scalef(0.8))
        .dot(rotf(- 30 * np.pi / 180))
        .dot(transf(-cx, -cy)))
    # print(A.shape)
    # plot a dot at the rotation center
    axes[0, 1].plot(cx, cy, 'r+')
    warped_im = warp_inbuilt.warp(im_gray, A, output_shape)

    axes[1, 0].imshow(warped_im, cmap=plt.get_cmap('gray'))
    axes[1, 0].set_title('warped')

    out_im = warp.warp(im_gray, A, output_shape)
    axes[1, 1].imshow(out_im, cmap=plt.get_cmap('gray'))
    axes[1, 1].set_title('output')

    # write the plot to an image
    plt.savefig(OUTPUT_IMG)
    print("DONE...")

if __name__ == "__main__":
    DATA_DIRECTORY = "data/"
    RESULTS_DIRECTORY = "warp_results/"
    if os.path.exists(RESULTS_DIRECTORY):
        shutil.rmtree(RESULTS_DIRECTORY)
    os.mkdir(RESULTS_DIRECTORY)
    INPUT_IMAGE = DATA_DIRECTORY + "mug.jpg"
    OUTPUT_IMAGE = RESULTS_DIRECTORY + "transformed.jpg"
    print("Run Affine Warping transformations......")
    main(INPUT_IMAGE, OUTPUT_IMAGE)
