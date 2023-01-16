function w = WTAcalc(Fa,Fb)
% Calculates WTA index with the firing rates of the two summation neurons
%   Closer to 1 means strong rivalry, closer to 0 means responses are
%   similar
e = 0.005;
frac = abs(Fa - Fb)./(e + Fa + Fb);
frac(isnan(frac)) = 0;
w = mean(frac);
end

