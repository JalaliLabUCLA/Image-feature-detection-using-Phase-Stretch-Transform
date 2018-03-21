#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementation of Phase Stretch Transform (PST) in Python
@author: Madhuri Suthar, Ph.D. candidate, Jalali Lab, Department of Electrical and Computer Engineering,  UCLA

PST or Phase Stretch Transform is a physics-inspired edge detection algorithm that detects intensity variations in an image [1,2]. 
PST operates on an input greyscale image and outputs an edge map. The output egde map, same as the size of the input image, is binary with 
pixel value equal to 1 where the PST operator finds sharp transitions in intensity and 0 elsewhere. The PST operator can also return 
a continous level edge map (i.e. without thresholding and morphological operations)

The PST operator cascades Gaussian smoothing, application of a nonlinear frequency-dependent phase kernel in frequency domain and a phase detection in spatial domain.
To implement the first step, an isotropic gaussian filter with a user defined scale (LPF) is designed and operated on the image. 
Next, a 2D PST phase kernel is designed in frequency domain and applied to the spectrum of the input image. The output of the transform is the
phase in the spatial domain. The amount of phase applied to the image is frequency dependent with higher amount of phase applied to higher frequency features of the
image. Since sharp transitions, such as edges and corners, contain higher frequencies, PST emphasizes the edge information. Features can
be further enhanced by applying thresholding and morphological operations.
For more information please visit: https://en.wikipedia.org/wiki/Phase_stretch_transform

[out PST_Kernel]= PST(Image,LPF,Phase_strength,Warp_strength, Threshold_min, Threshold_max, Morph_flag) takes the image I and applies
PST phase kernel parameters are described as follows:

Parameters
----------
LPF            : Isotropic Gaussian localization filter Full Width at Half Maximum (FWHM) (min : 0, max : 1)
Phase_strength : PST Kernel Phase Strength (min : 0, max : 1)
Warp_strength  : PST Kernel Warp Strength (min : 0, max : 1)
Threshold_min  : minimum threshold  (min : -1, max : 0)
Threshold_max  : maximum threshold  (min : 0, max : 1)
Morph_flag allows user to compute the analog edge (if Morph_flag=0) or the digital edge (analog edge followed
by thresholding and morphological operations, if Morph_flag=1).                                                    

Copyright
---------
PST function  is developed in Jalali Lab at University of California,
Los Angeles (UCLA).  PST is a spin-off from research on the photonic time stretch technique in Jalali lab at UCLA.
More information about the technique can be found in our group
website: http://www.photonics.ucla.edu
This function is provided for research purposes only. A license must be
obtained from the University of California, Los Angeles for any commercial
applications. The software is protected under a US patent.
 
Citations
---------
1. M. H. Asghari, and B. Jalali, "Edge detection in digital images using dispersive phase stretch," International Journal of Biomedical Imaging, Vol. 2015, Article ID 687819, pp. 1-6 (2015).
2. M. H. Asghari, and B. Jalali, "Physics-inspired image edge detection," IEEE Global Signal and Information Processing Symposium (GlobalSIP 2014), paper: WdBD-L.1, Atlanta, December 2014.
3. M. Suthar, H. Asghari, and B. Jalali, "Feature Enhancement in Visually Impaired Images", IEEE Access 6 (2018): 1407-1415.
4. Y. Han, and B. Jalali, "Photonic time-stretched analog-to-digital converter: Fundamental concepts and practical considerations", Journal of Lightwave Technology 21, no. 12 (2003): 3085.
"""
# Imports
# [] Need to install mahotas library for morphological operations
import os 
import numpy as np
import mahotas as mh
import matplotlib.pylab as plt
from itertools import zip_longest
from PST_function import PST

# [] To process high resolution images set 
# from PIL import Image
# Image.MAX_IMAGE_PIXELS = 1000000000
# Replace mh.imread by Image.open

# import sys
# [] To input filename using command line argument uncomment ^^^


# Import the original image
input_path = os.getcwd() # This is where the code is running. 
filepath = os.path.join(input_path,'../Test_Images/cameraman.tif')  # The images are located in a folder called 'Test_Images' within the root directory from where the code runs.

#filepath = os.path.join(input_path,'../Test_Images/',sys.argv[1])
# [] To input filename using command line argument uncomment ^^^

Image_orig = mh.imread(filepath) # Read the image.
# To convert the color image to greyscale
if Image_orig.ndim ==3:
    Image_orig_grey = mh.colors.rgb2grey(Image_orig)  # Image_orig is color image.
else: 
    Image_orig_grey = Image_orig
    
# Define various 
# low-pass filtering (also called localization kernel) parameter
LPF = 0.21 # Gaussian Low Pass Filter
# PST parameters
Phase_strength = 0.48 
Warp_strength= 12.14
# Thresholding parameters (for post processing after the edge is computed)
Threshold_min = -1
Threshold_max = 0.0019
# [] Choose to compute the analog or digital edge,
Morph_flag =1 # [] To compute analog edge, set Morph_flag=0 and to compute digital edge, set Morph_flag=1

 
[Edge, PST_Kernel]= PST(Image_orig_grey, LPF, Phase_strength, Warp_strength, Threshold_min, Threshold_max, Morph_flag)

if Morph_flag ==0:
    Edge = (Edge/np.max(Edge))*3
    # Display results    
    def imshow_pair(image_pair, titles=('', ''), figsize=(6, 6), **kwargs):
        fig, axes = plt.subplots(ncols=len(image_pair), figsize=figsize)
        for ax, img, label in zip_longest(axes.ravel(), image_pair, titles, fillvalue=''):
            ax.imshow(img, **kwargs)
            ax.set_title(label)
    # show the original image and detected edges
    print('        Original Image       Edge Detected using PST')
    imshow_pair((Image_orig, Edge), cmap='gray')
    
    # Save results
    default_directory, filename=filepath.split('./Test_Images/')
    filename, extension = filename.split('.')
    output_path=default_directory+'./Test_Images/'+filename+'_edge.tif' # Saving the edge map with the extension tiff
    mh.imsave(output_path, Edge)
   
else:
    Overlay=mh.overlay(Image_orig,Edge)
  
    # Display results    
    def imshow_pair(image_pair, titles=('', ''), figsize=(10, 6), **kwargs):
        fig, axes = plt.subplots(ncols=len(image_pair), figsize=figsize)
        for ax, img, label in zip_longest(axes.ravel(), image_pair, titles, fillvalue=''):
            ax.imshow(img, **kwargs)
            ax.set_title(label)
    # show the original image, detected edges and an overlay of the original image with detected edges       
    print('      Original Image            Edge Detected using PST              Overlay')
    imshow_pair((Image_orig, Edge, Overlay), cmap='gray')
    
    # Save results
    default_directory, filename=filepath.split('./Test_Images/')
    filename, extension = filename.split('.')
    output_path=default_directory+'./Test_Images/'+filename+'_edge.tif' # Saving the edge map with the extension tiff
    mh.imsave(output_path, Edge.astype(np.uint8)*255)
    output_path=default_directory+'./Test_Images/'+filename+'_overlay.tif' # Saving the overlay with the extension tiff
    mh.imsave(output_path, Overlay)

