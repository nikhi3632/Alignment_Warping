import numpy as np
import skimage as sk
import math

# Crops the borders of a given images by a constant factor given "percentage"
def crop_borders(img, percentage):
	x_crop = int(percentage*img.shape[0]/2)
	y_crop = int(percentage*img.shape[1]/2)
	return img[x_crop:img.shape[0]-x_crop,y_crop:img.shape[1]-y_crop]

# Translates an image by (dx,dy)
def img_translate(img,dx,dy):
	result = np.roll(img, (dy, dx), axis=(0, 1))
	return result

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

# Given two images, find the best alignment for image 1 compared to image 2, given
# a heuristic to compare two images (In this case, the NSSD)
def best_alignment(img_1, img_2, heuristic, displacement):
	# Best alignments so far
	best_value = np.inf
	best_dx = 0
	best_dy = 0
	# Defines a search window of displacements of [-30,30] for each direction.
	# For images that do not have more than 30 pixels of width and height, stick
	# lower the window to their resolution
	width_search_window = int(min(displacement,img_1.shape[0]/2))
	height_search_window = int(min(displacement,img_1.shape[1]/2))
	for dx in range(-width_search_window,width_search_window):
		for dy in range(-height_search_window,height_search_window):
			nssd = heuristic(img_translate(img_1,dx,dy),img_2)
			if nssd < best_value:
				best_value = nssd
				best_dx = dx
				best_dy = dy
	return (best_dx, best_dy)

# Multi Scale Alignment. Given two image pyramids, find the best alignment for image 1 compared to image 2, 
# given a heuristic to compare two images (In this case, the NSSD)

def align_pyramids(_pyramid_img_1, pyramid_img_2, heuristic, crop_percentage, displacement, scale):
	# First, copy the first image pyramid to be sure we will not overwrite any input data.
	pyramid_img_1 = _pyramid_img_1
	# Best alignments so far
	best_dx, best_dy = 0, 0
	# Level by level, try to align the images using the single scale alignment
	for image_1, image_2 in zip(reversed(pyramid_img_1), reversed(pyramid_img_2)):
		# Whatever was the best alignment received from the last level, scale it
		# This must be done because the amount of pixels in the new levels will be larger
		# This factor of scale takes that in consideration for the aligment
		best_dx *= scale
		best_dy *= scale
		# Translates the current image with the best alignment found
		image_1 = img_translate(image_1,best_dx,best_dy)
		# Crops the image to make sure we get rid of the noisy borders
		image_1 = crop_borders(image_1, crop_percentage)
		image_2 = crop_borders(image_2, crop_percentage)
		# Align the image with the single scale alignment
		new_dx, new_dy = best_alignment(image_1,image_2,heuristic,displacement)
		best_dx += new_dx
		best_dy += new_dy
	# translates the original image using the best alignment found
	return (img_translate(pyramid_img_1[0],best_dx,best_dy),[best_dx,best_dy])

# Given a image, creates its image pyramid
def create_pyramid(img, scale):
	# Calculate in how many levels each dimension can be divided into
	width_dim = int(math.log(img.shape[0],scale))
	height_dim = int(math.log(img.shape[1],scale))
	# The number of levels in the image will be the minimum of width, height
	num_images = min(width_dim,height_dim)
	# Initializes the image array
	pyramid = []
	# Adds the original image as the 'level 0' image
	pyramid.append(np.asarray(img))
	# Generate each level by using a rescaled version of the previous level
	# Information is lost on every level
	for i in range(1,num_images+1):
		pyramid.append(sk.transform.rescale(pyramid[i-1],(1.0/scale)))
	return pyramid

# Align the red, green and blue channels comparing them to the green image
def align_channels(r, g, b, crop_percentage = 0.25, displacement = 30, scale = 2):
	# Defines the heuristic to use
	heuristic = calculate_NSSD
	# Create the pyramids
	assert isinstance(crop_percentage, float)
	assert isinstance(displacement, int)
	assert isinstance(scale, int)
	print ("Creating red image pyramid...")
	pyramid_r = create_pyramid(r, scale)
	print ("Creating green image pyramid...")
	pyramid_g = create_pyramid(g, scale)
	print ("Creating blue image pyramid...")
	pyramid_b = create_pyramid(b, scale)
	# Find the best alignments based on the pyramids
	print ("Aligning the red image compared to the green image (wait)...")
	aligned_r, r_d = align_pyramids(pyramid_r, pyramid_g, heuristic, crop_percentage, displacement, scale)
	aligned_g, g_d = pyramid_g[0], [0, 0]
	print ("Aligning the blue image compared to the green image (wait)...")
	aligned_b, b_d = align_pyramids(pyramid_b, pyramid_g, heuristic, crop_percentage, displacement, scale)
	print ("Alignment Complete !!! Results:")
	print ("R Alignment = (" + str(r_d[0]) + "," + str(r_d[1]) + ")")
	print ("G Alignment = (" + str(g_d[0]) + "," + str(g_d[1]) + ") (Reference)")
	print ("B Alignment = (" + str(b_d[0]) + "," + str(b_d[1]) + ")")
	print ("Cropping borders by {}%...".format(crop_percentage*100))
	aligned_r = crop_borders(aligned_r, crop_percentage)
	aligned_g = crop_borders(aligned_g, crop_percentage)
	aligned_b = crop_borders(aligned_b, crop_percentage)
	print ("Stacking processed images...")
	output_image_aligned = np.dstack([aligned_r, aligned_g, aligned_b])
	print ("DONE!")
	return output_image_aligned
