function f = Delta(phi, sigma)
%   Delta(phi, epsilon) compute the smooth Dirac function
%  
%   created on 04/26/2004
%   author: Chunming Li
%   email: li_chunming@hotmail.com
%   Copyright (c) 2004-2006 by Chunming Li

f=(1/2/sigma)*(1+cos(pi*phi/sigma));
b = (phi<=sigma) & (phi>=-sigma);
f = f.*b;
