function N = createOrnsteinGaussKern(n,p)
% calculation of Ornstein-Uhlenbeck process with Gaussian kernel
%   calculation a priori for entire time
%   Gaussian kernel (positive part) as low-pass filter
whiteNoise = p.varNoise .* randn(n,p.numSteps);
impResp = normpdf(0:p.dt:p.T,0,p.varImpResp);
impResp = impResp/norm(impResp);
fft_impResp = fft(impResp);
N = zeros(n,p.numSteps);
for i = 1:n
    fft_N = fft(whiteNoise(i,:));
    N(i,:) = ifft(fft_N .* fft_impResp);
end
end