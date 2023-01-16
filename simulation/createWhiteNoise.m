function N = createWhiteNoise(n,p)
% calculation of Gaussian white noise process
%   calculation a priori for entire time
%   no temporal correlation
N = p.varNoise .* randn(n,p.numSteps);
end