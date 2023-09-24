import numpy as np

def warp(im, A, output_shape):
    """ Warps (h,w) image im using affine (3,3) matrix A
    producing (output_shape[0], output_shape[1]) output image
    with warped = A*input, where warped spans 1...output_size.
    Uses nearest neighbor interpolation."""
    row, col = np.mgrid[0:output_shape[0], 0:output_shape[1]]
    A_inverse = np.linalg.inv(A)
    X = np.round(A_inverse[1, 0]*row + A_inverse[1, 1]*col + A_inverse[1, 2]).astype(int)
    Y = np.round(A_inverse[0, 0]*row + A_inverse[0, 1]*col + A_inverse[0, 2]).astype(int)
    height, width = im.shape
    X[(X < 0) | (X >= width)] = width
    Y[(Y < 0) | (Y >= height)] = height
    return np.pad(im, ((0, 1), (0, 1)))[(Y, X)]
