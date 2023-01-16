%%% Parameters of model %%%
c               = .5; %contrast
sigma           = .5; %semisaturation constant
sigma_opp       = .9; %semisaturation constant for opponency cells

p.varNoise      = 0.05; %noise intensity
p.varImpResp    = 500; %temporal correlation of OU noise (ms)

p.s             = [sigma,sigma,sigma,sigma,sigma_opp,sigma_opp,sigma_opp,sigma_opp,sigma,sigma]; %semisaturation constant
p.tau           = 50; %time constant (ms)
p.T             = 60000; %duration (ms)
p.I             = [c 0 0 c 0 0 0 0 0 0]; %input vector for dichoptic gratings
p.varNoise      = 0.03; %variance of Gaussian white noise
p.varImpResp    = 800; %variance of (Gaussian) impulse response (ms)
p.dt            = 5; %time step (ms) - for noise only
p.numSteps      = p.T/p.dt + 1; %number of steps
p.tol           = 1e-2; %tolerance to find zeros of FA-FB
p.duratLim      = 300; %minimum duration of a rivalry epoch (ms)
p.wtaLim        = 0.5; %minimum WTA index of a rivalry epoch
p.tauh          = 2000; % time constant of adaptation (ms)
p.wh            = 2; % weight of adaptation



NoiseSwitch = 3;
if NoiseSwitch == 0
    fprintf("\nOrnstein-Uhlenbeck noise, with Gaussian kernel as low-pass filter.\n");
elseif NoiseSwitch == 1
    fprintf("\nOrnstein-Uhlenbeck noise, with exponential kernel as low-pass filter.\n");
elseif NoiseSwitch == 2
    fprintf("\nGaussian white noise, with no temporal correlation, used.\n");
elseif NoiseSwitch == 3
    fprintf("\nPink (1/f) noise used.\n");
else
    fprintf("\nError setting up noise.\n");
end

%%% Call to simulation %%%

PlotSwitch = 1; % 0 to suppress plot
[WTA,PercRivalry,meanDur,CV,meanDurMix] = model_core(p,0,NoiseSwitch);

%%% Print metrics %%%

params   = sprintf("Noise Intensity = %.3f\nNoise Correlation Time = %d ms\nInput Contrast = %.2f",p.varNoise,p.varImpResp,p.I(1));
str_wta  = sprintf("\nWTA = %.2f",WTA);
str_prop = sprintf("PDT = %d%%",round(PercRivalry));
str_d    = sprintf("Mean Duration = %.2f s",meanDur);
str_c    = sprintf("Coefficient of Variation of Durations = %f\n",round(CV,2));
str_dm   = sprintf("Mean Mixed Duration = %.2f s",meanDurMix);
disp(params)
disp(str_wta)
disp(str_prop)
disp(str_d)
disp(str_c)
disp(str_dm)