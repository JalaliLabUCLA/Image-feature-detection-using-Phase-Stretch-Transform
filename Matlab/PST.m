% Implementation of Phase Stretch Transform (PST) in Matlab
% author: M. Asghari, Jalali Lab, Department of Electrical and Computer Engineering,  UCLA
function [out PST_Kernel]= PST(I,handles,Morph_flag)
%PST or Phase Stretch Transform is an operator that finds features in an
%   image. PST takes an intensity image I as its input, and returns a
%   binary image out of the same size as I, with 1's where the function finds sharp transitions in 
%   I and 0's elsewhere. PST function is also able to return the detected features in gray scale 
%   level (i.e. without thresholding).
%
%   In PST, the image is first filtered by passing through a smoothing
%   filter followed by application of a nonlinear frequency-dependent phase
%   described by the PST phase kernel. The output of the transform is the
%   phase in the spatial domain. The main step is the 2-D phase function
%   (PST phase kernel) which is typically applied in the frequency domain.
%   The amount of phase applied to the image is frequency dependent with
%   higher amount of phase applied to higher frequency features of the
%   image. Since sharp transitions, such as edges and corners, contain
%   higher frequencies, PST emphasizes the edge information. Features can
%   be further enhanced by applying thresholding and morphological operations.
%   For more information please visit: https://en.wikipedia.org/wiki/Phase_stretch_transform
%
%   [out PST_Kernel]= PST(I,handles, Morph_flag) takes the original image I and applies
%   PST to it. PST kernel paramters are given using a handle variable:
%
%   handles.LPF            : Gaussian low-pass filter Full Width at Half Maximum (FWHM) (min : 0, max : 1)
%   handles.Phase_strength : PST  kernel Phase Strength (min : 0, max : 1)
%   handles.Warp_strength  : PST Kernel Warp Strength (min : 0, max : 1)
%   handles.Thresh_min     : minimum Threshold  (min : -1, max : 0)
%   handles.Thresh_max     : maximum Threshold  (min : 0, max : 1)
%
%   Morph_flag allows user to compute the analog edge (if Morph_flag=0) or the digital edge (analog edge followed
%   by thresholding and morphological operations)(if Morph_flag=1).
%
%   Class Support
%   -------------
%   I is a double precision 2D array. out is of class logical.
%
%   Remarks
%   -------
%   image processing toolbox is needed to run this function, function has
%   been tested on MATLAB R2013a on a computer with Windows 7, 64 bits operating sytsem.
%   The code uses IMOVERLAY function deveopled by Steven L. Eddins for visulaization of detected features.
%
%   Example
%   -------
%   Example 1: Find the features of the circuit.tif image using PST method:
%
%      I = imread('circuit.tif');
%      I=double(I);
%      handles.LPF=0.21;
%      handles.Phase_strength=0.48;
%      handles.Warp_strength=12.14;
%      handles.Thresh_min=-1;
%      handles.Thresh_max=0.004;
%      [out PST_Kernel]= PST(I,handles);
%      figure, imshow(out)
%
%   Example 2: Find the features in the Lena image. See the attached test script.
%   
%   Copyright
%   ---------
%   PST function  is developed in Jalali Lab at University of California,
%   Los Angeles (UCLA).  PST is a spin-off from research on the photonic time stretch technique in Jalali lab at UCLA.
%   More information about the technique can be found in our group
%   website: http://www.photonics.ucla.edu
%   This function is provided for research purposes only. A license must be
%   obtained from the University of California, Los Angeles for any commercial
%   applications. The software is protected under a US patent.
%   Citations:
%   1. M. H. Asghari, and B. Jalali, "Edge detection in digital images using dispersive phase stretch," International Journal of Biomedical Imaging, Vol. 2015, Article ID 687819, pp. 1-6 (2015).
%   2. M. H. Asghari, and B. Jalali, "Physics-inspired image edge detection," IEEE Global Signal and Information Processing Symposium (GlobalSIP 2014), paper: WdBD-L.1, Atlanta, December 2014.
%   3. M. Suthar, H. Asghari, and B. Jalali, "Feature Enhancement in Visually Impaired Images", IEEE Access 6 (2018): 1407-1415.
%   4. Y. Han, and B. Jalali, "Photonic time-stretched analog-to-digital converter: Fundamental concepts and practical considerations", Journal of Lightwave Technology 21, no. 12 (2003): 3085.
%   Copyright 1992-2016 The MathWorks, Inc.
%   $Revision: 0.0.0.1 $  $Date: 2016/02/09 13:20:56 $

% define two dimentional cartesian (rectangular) vectors, X and Y
Image_orig_size=size(I);
L=0.5;
x=linspace(-L,L,Image_orig_size(1));
y=linspace(-L,L,Image_orig_size(2));
[X,Y]=ndgrid(x,y);

% Convert cartesian X and Y vectors to polar vectors, THETA and RHO
[THETA,RHO] = cart2pol(X,Y);

% define two dimentional cartesian frequency vectors, FX and FY
X_step=x(2)-x(1);
fx=linspace(-0.5/X_step,0.5/X_step,length(x));
fx_step=fx(2)-fx(1);
Y_step=y(2)-y(1);
fy=linspace(-0.5/Y_step,0.5/Y_step,length(y));
fy_step=fy(2)-fy(1);
[FX,FY]=ndgrid(fx,fy);

% Convert cartesian vectors (FX and FY) to polar vectors, FTHETA and FRHO
[FTHETA,FRHO] = cart2pol(FX,FY);

% low pass filter the original image to reduce noise
Image_orig_f=((fft2(I)));
sigma=(handles.LPF)^2/log(2);
Image_orig_f=Image_orig_f.*fftshift(exp(-(RHO/sqrt(sigma)).^2));
Image_orig_filtered=real(ifft2((Image_orig_f)));

% Constrcut the PST Kernel
PST_Kernel=(RHO*handles.Warp_strength.*atan(RHO*handles.Warp_strength)-0.5*log(1+(RHO*handles.Warp_strength).^2));
PST_Kernel=PST_Kernel/max(max(PST_Kernel))*handles.Phase_strength;

% Apply the PST Kernel
temp=(fft2(Image_orig_filtered)).*fftshift(exp(-1j*PST_Kernel));
Image_orig_filtered_PST=ifft2(temp);

% Calculate phase of the transformed image
PHI_features=angle(Image_orig_filtered_PST);

if Morph_flag ==0
    out=PHI_features;
else
    % find image sharp transitions by thresholding the phase
    features=zeros(size(PHI_features));
    features(find(PHI_features>handles.Thresh_max))=1;
    features(find(PHI_features<handles.Thresh_min))=1;  % because output phase has both positive and negative values
    features(find(I<max(max(I))/20))=0; % ignore the features in the very dark areas of the image
    
    % apply binary morphological operations to clean the transformed image
    out=features;
    out = bwmorph(out,'thin',1);
    out = bwperim(out,4);
    out = bwmorph(out,'thin',1);
    out = bwmorph(out,'clean',30);
    out = bwmorph(out,'remove',5);
    
end

