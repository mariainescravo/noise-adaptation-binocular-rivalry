function N = createOrnsteinExpKern(n,p)
% calculation of Ornstein-Uhlenbeck process with exponential kernel
%   calculation a priori for entire time
%   exponential kernel as low-pass filter
whiteNoise = p.varNoise .* randn(n,p.numSteps);
impResp = exp(-(0:p.dt:p.T)/p.varImpResp )/p.varImpResp;
impResp = impResp/norm(impResp);
fft_impResp = fft(impResp);
N = zeros(n,p.numSteps);
for i = 1:n
    fft_N = fft(whiteNoise(i,:));
    N(i,:) = ifft(fft_N .* fft_impResp);
end
end
