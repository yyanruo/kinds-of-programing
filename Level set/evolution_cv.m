function phi = EVOLUTION_CV(I, phi0, g, mu, nu, lambda, delta_t, epsilon, numIter);
%   evolution_withoutedge(I, phi0, mu, nu, lambda_1, lambda_2, delta_t, delta_h, epsilon, numIter);
%   input: 
%       I: input image
%       phi0: level set function to be updated
%       mu: weight for length term
%       nu: weight for area term, default value 0
%       lambda_1:  weight for c1 fitting term
%       lambda_2:  weight for c2 fitting term
%       delta_t: time step
%       epsilon: parameter for computing smooth Heaviside and dirac function
%       numIter: number of iterations
%   output: 
%       phi: updated level set function
%  
%   created on 04/26/2004
%   author: Chunming Li
%   email: li_chunming@hotmail.com
%   Copyright (c) 2004-2006 by Chunming Li

  
I = BoundMirrorExpand(I); % ????????????
phi = BoundMirrorExpand(phi0);
g = BoundMirrorExpand(g);
for k = 1 : numIter
    phi = BoundMirrorEnsure(phi);
    phi = NeumannBoundCond(phi);
    delta_h = Delta(phi,epsilon);
    Curv = curvature(g,phi);
    Curv1 = curvature1(phi);
 
    
    % updating the phi function
    phi=phi+delta_t*(mu*(4*del2(phi)-Curv1)+lambda*delta_h.*Curv+delta_h.*g.*nu);    
end
phi = BoundMirrorShrink(phi); % ??????????????


function g = NeumannBoundCond(f)
% Make a function satisfy Neumann boundary condition
[nrow,ncol] = size(f);
g = f;
g([1 nrow],[1 ncol]) = g([3 nrow-2],[3 ncol-2]);  
g([1 nrow],2:end-1) = g([3 nrow-2],2:end-1);          
g(2:end-1,[1 ncol]) = g(2:end-1,[3 ncol-2]);  