function N = createPinkNoise(n,p)
% calculation of 1/f (pink) noise process
%   calculation a priori for entire time
%   randomness introduced in phase

Fmax = 1/(2*p.dt); % maximum frequency of spectrum
M = p.numSteps; % number of samples
df   = Fmax/M; % interval of sampling in frequency domain
f = df:df:Fmax; % starts at df to avoid dividing by zero later on

PSD = 1./f; % pink noise power spectral density function
A = sqrt(2*PSD); % convert from power to amplitude

phi = zeros(n,M);
for i = 1:n
    phi(i,:) = 2*pi*rand(1,M); % assign random phase to each spectral component
end

Z = A .* exp(1i * phi); % construct frequency domain signal

N = real(ifft(Z'));
N = N';

sd_noise = mean(std(N,0,2));
scaling_factor = p.varNoise/sd_noise;
N = scaling_factor * N;

end