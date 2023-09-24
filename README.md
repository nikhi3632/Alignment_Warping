# Color Channel Alignment and Image Warping

To see it in action, git clone the repo and 
```bash
chmod +x run_*.sh
./run_all.sh
```
To do clean up
```bash
chmod +x clean.sh
./clean.sh
```

# Color Channel Alignment

Given a red, green, and blue channels of an image that were taken separately using an old technique that captured each color on a separate piece of glass, since these images were taken separately, just combining them in a 3-channel matrix may not work if you simply combine the images without shifting any of the channels. The easiest way to do align the color channels is to exhaustively search over a window of possible displacements for the different channels. Score the alignment from each possible displacement with some heuristic and choose the best alignment using these scores.

The individual channels are shown below

<img src="explore/channels.jpg">

Combining the red, green, and blue channels without shifting

<img src="explore/no_shift.jpg">

A better image can be achieved by using alignment, pyramids and cropping the edges

<img src="align_results/aligned_output.jpg">

# Image Warping

Affine Transformation

<img src="imgs/math.jpeg">

Given image

<img src="data/mug.jpg">

Generating affine transformations of the given image

<img src="warp_results/transformed.jpg">
