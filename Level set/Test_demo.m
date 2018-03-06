%   Matlad code implementing Chan-Vese model in the paper 'Active Contours Without Edges'
%   This method works well for bimodal images, for example the image 'three.bmp'


clear;
close all;
clc;

%Img=imread('three.bmp');     % example that CV model works well
%Img=imread('vessel.bmp');    % example that CV model does NOT work well
Img=imread('twoCells.bmp');  % example that CV model does NOT work well
I=double(Img(:,:,1));
U=Img(:,:,1);

% get the size
[nrow,ncol] =size(U);

ic=nrow/2;
jc=ncol/2;
r=30;
phi_0 = sdf2circle(nrow,ncol,ic,jc,r);
figure; mesh(phi_0); title('Signed Distance Function')

delta_t = 5.0;
lambda =5.0;
mu = 0.04
nu = 1.5;
epsilon=1;

sigma=1.5;     % scale parameter in Gaussian kernel
G=fspecial('gaussian',15,sigma);
Img_smooth=conv2(I,G,'same');  % smooth image by Gaussiin convolution
[Ix,Iy]=gradient(Img_smooth);
f=Ix.^2+Iy.^2;
g=1./(1+f);  % edge indicator function.

I=double(U);
% iteration should begin from here
phi=phi_0;
figure(2);
imagesc(uint8(I));colormap(gray)
hold on;
plotLevelSet(phi,0,'r');

numIter = 1;
for k=1:1000,
    phi = evolution_cv(I, phi, g, mu, nu, lambda, delta_t, epsilon, numIter);   % update level set function
    if mod(k,20)==0
        pause(.0005);
        imagesc(uint8(I));colormap(gray)
        figure(2); hold on;
        plotLevelSet(phi,0,'r');
    end    
end;
