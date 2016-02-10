# Image-feature-detection-using-Phase-Stretch-Transform
PST or Phase Stretch Transform is an operator that finds features in an image. PST takes an intensity image I as its input, and returns a   binary image out of the same size as I, with 1's where the function finds sharp transitions in I and 0's elsewhere. PST function is also able to return the detected features in gray scale level (i.e. without thresholding).
In PST, the image is first filtered by passing through a smoothing  filter followed by application of a nonlinear frequency-dependent phase  described by the PST phase kernel. The output of the transform is the  phase in the spatial domain. The main step is the 2-D phase function   (PST phase kernel) which is typically applied in the frequency domain.   The amount of phase applied to the image is frequency dependent with  higher amount of phase applied to higher frequency features of the  image. Since sharp transitions, such as edges and corners, contain  higher frequencies, PST emphasizes the edge information. Features can   be further enhanced by applying thresholding and morphological operations.
For more information please visit: https://en.wikipedia.org/wiki/Phase_stretch_transform

[out PST_Kernel]= PST(I,handles, Morph_flag) takes the original image I and applies
PST to it. PST kernel paramters are given using a handle variable:
handles.LPF            : Gaussian low-pass filter Full Width at Half Maximum (FWHM) (min : 0, max : 1)
handles.Phase_strength : PST  kernel Phase Strength (min : 0, max : 1)
handles.Warp_strength  : PST Kernel Warp Strength (min : 0, max : 1)
handles.Thresh_min     : minimum Threshold  (min : -1, max : 0)
handles.Thresh_max     : maximum Threshold  (min : 0, max : 1)

Morph_flag allows user to compute the analog edge (if Morph_flag=0) or the digital edge (analog edge followed
by thresholding and morphological operations)(if Morph_flag=1).

Remarks
Image processing toolbox is needed to run this function, function has  been tested on MATLAB R2013a on a computer with Windows 7, 64 bits operating sytsem.  The code uses IMOVERLAY function deveopled by Steven L. Eddins for visulaization of detected features.

Copyright
PST function  is developed in Jalali Lab at University of California,  Los Angeles (UCLA).  PST is a spin-off from research on the photonic time stretch technique in Jalali lab at UCLA.  More information about the technique can be found in our group  website: http://www.photonics.ucla.edu
This function is provided for research purposes only. A license must be  obtained from the University of California, Los Angeles for any commercial  applications. The software is protected under a US patent.
Citations:
1. M. H. Asghari, and B. Jalali, "Edge detection in digital images using dispersive phase stretch," International Journal of Biomedical Imaging, Vol. 2015, Article ID 687819, pp. 1-6 (2015).
2. M. H. Asghari, and B. Jalali, "Physics-inspired image edge detection," IEEE Global Signal and Information Processing Symposium (GlobalSIP 2014), paper: WdBD-L.1, Atlanta, December 2014.
