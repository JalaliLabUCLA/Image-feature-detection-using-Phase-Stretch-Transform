# Instructions for Python 3.x 
#
## Prerequisites
##
You can install most of the following packages using pip.
* NumPy
* Python Imaging Library (PIL)
* Matplotlib
* Itertools
* Mahotas 

## Remarks
##
Mahotas library is needed to implement morphological operations and display overlay in case of digital edge detection (if Morph_flag==1).

## Testing
##
Put your test images in the Test_Images directory and then, set the file path in the code on line 70. You can also pass the filename using the command line [Uncomment lines 64 and 72 and comment line 70].
The images can be color or greyscale. However, PST operation occurs on color images only after converting them to greyscale. You can change the filename in the test_script_PST.py code to run the algorithm on the test image. 

## Visualization
##
The code uses matplotlib and mahouts to visualize PST edge map and overlay (in case of digital edge). [See section # Display results in test_script_PST.py]

## Test Results
The PST edge map and overlay (in case of digital edge when Morph_flag==1) are saved in the Test_Images folder. [See section # Save results test_script_PST.py]

## Copyright
##
PST function is developed in Jalali Lab at University of California,  Los Angeles (UCLA).  PST is a spin-off from research on the photonic time stretch technique in Jalali lab at UCLA.  More information about the technique can be found on our group  website: http://www.photonics.ucla.edu 
This function is provided for research purposes only. A license must be  obtained from the University of California, Los Angeles for any commercial  applications. The software is protected under a US patent.


## Citations
##
1. M. H. Asghari, and B. Jalali, "Edge detection in digital images using dispersive phase stretch," International Journal of Biomedical Imaging, Vol. 2015, Article ID 687819, pp. 1-6 (2015).
2. M. H. Asghari, and B. Jalali, "Physics-inspired image edge detection," IEEE Global Signal and Information Processing Symposium (GlobalSIP 2014), paper: WdBD-L.1, Atlanta, December 2014.
3. M. Suthar, H. Asghari, and B. Jalali, "Feature Enhancement in Visually Impaired Images", IEEE Access 6 (2018): 1407-1415.
4. Y. Han, and B. Jalali, "Photonic time-stretched analog-to-digital converter: Fundamental concepts and practical considerations", Journal of Lightwave Technology 21, no. 12 (2003): 3085.

Copyright (c) 2016, Jalali Lab All rights reserved.
