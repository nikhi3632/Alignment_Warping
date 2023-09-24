import numpy as np
import matplotlib.pyplot as plt
import os

def align_channels(red, green, blue, shift):
  """
  Given 3 images corresponding to different channels of a color image,
  compute the best aligned result with minimum abberations

  Args:
    red, green, blue - each is a HxW matrix corresponding to an HxW image
    shift - exhaustively search over a window of possible displacements for the different channels
  Returns:
    rgb_output - HxWx3 color image output, aligned as desired
  """
  return None