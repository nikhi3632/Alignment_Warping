import numpy as np
import matplotlib.pyplot as plt
import os
import imageio
from PIL import Image
import warnings
warnings.filterwarnings("ignore")

def calculate_NSSD(u, v):
  '''
  u : A numpy array that represents the pixel values of one image (e.g., a grayscale or color image). 
    It's the reference image against which to compare another image y.
  v : Another numpy array that represents the pixel values of the second image 
    (typically aligned or transformed) that you want to compare with the reference image x.
  Normalized Sum of Squared Differences, Measures structural dissimilarity.
  '''
  # Ensure that both arrays have the same shape
  if u.shape == v.shape:
    ssd = np.sum((u - v)**2)
    num_pixels = u.size
    return (np.sqrt(ssd))/(num_pixels)
  else:
    raise ValueError("Input arrays must have the same shape")

def align_channels(red, green, blue):
  """
  Given 3 images corresponding to different channels of a color image,
  compute the best aligned result with minimum abberations

  Args:
    red, green, blue - each is a HxW matrix corresponding to an HxW image
    shift - exhaustively search over a window of possible displacements for the different channels
  Returns:
    rgb_output - HxWx3 color image output, aligned as desired
  """
  None