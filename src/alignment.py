from align_channels import align_channels
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
import imageio
from PIL import Image

def explore(npys_dir, EXPLORE_DIR):
  cwd = os.getcwd()
  rgb_npy_files = [file for file in os.listdir(npys_dir) if file.endswith('.npy') and (file.startswith('red') or file.startswith('green') or file.startswith('blue'))]
  num_images = len(rgb_npy_files)
  _, axes = plt.subplots(1, num_images, figsize=(12, 6))
  for i, file in enumerate(rgb_npy_files):
      data = np.load(os.path.join(npys_dir, file))
      ax = axes[i]
      ax.imshow(data, cmap='brg')
      ax.set_title(file.split(".")[0])
      ax.axis('off')
  plt.tight_layout()
  if not os.path.exists(cwd + '/' + EXPLORE_DIR):
     os.mkdir(cwd + '/' + EXPLORE_DIR)
  plt.savefig(os.path.join(cwd + '/' + EXPLORE_DIR, "channels.jpg"), bbox_inches='tight')
  color_channels = [np.load(npys_dir + '/' + color_file) for color_file in rgb_npy_files]
  '''
  Combine the color channels to create an RGB image. In the context of color images, the
  third axis corresponds to the color channels, so stacking along axis=2. Same as np.dstack.
  '''
  rgb_image = np.stack(color_channels, axis=2)
  imageio.imwrite(os.path.join(EXPLORE_DIR, "no_shift.jpg"), rgb_image)
  image = Image.open(EXPLORE_DIR + "no_shift.jpg")
  image_array = np.array(image)
  np.save(os.path.join(EXPLORE_DIR, 'no_shift.npy'), image_array)

# Image Alignment
def main(DATA_DIR, RESULT_DIR):
    # 1. Load images (all 3 channels)
    red = np.load(DATA_DIR + 'red.npy')
    green = np.load(DATA_DIR + 'green.npy')
    blue = np.load(DATA_DIR + 'blue.npy')

    # 2. Find best channels alignment
    rgbResult = align_channels(red, green, blue)

    # 3. save result to rgb_output.jpg (IN THE "results" FOLDER)
    imageio.imwrite(RESULT_DIR + "aligned_output.jpg", rgbResult)
    image = Image.open(RESULT_DIR + "aligned_output.jpg")
    image_array = np.array(image)
    np.save(os.path.join(RESULT_DIR, 'aligned_output.npy'), image_array)

if __name__ == "__main__":
    # Setup dirs
    CWD = os.getcwd()
    DATA_DIRECTORY = "data/"
    EXPLORE_DIR = 'explore/'
    explore(DATA_DIRECTORY, EXPLORE_DIR)
    RESULTS_DIRECTORY = "align_results/"
    if os.path.exists(RESULTS_DIRECTORY):
        shutil.rmtree(os.path.join(CWD, RESULTS_DIRECTORY))
    os.mkdir(RESULTS_DIRECTORY)
    print('Run alignment......')
    main(DATA_DIRECTORY, RESULTS_DIRECTORY)
