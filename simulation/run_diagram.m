%%% Parameters of model %%%
c               = .5; %contrast
sigma           = .5; %semisaturation constant
sigma_opp       = .9; %semisaturation constant for opponency cells

p.varNoise      = 0.03; %noise intensity
p.varImpResp    = 800; %temporal correlation of OU noise (ms)

p.s             = [sigma,sigma,sigma,sigma,sigma_opp,sigma_opp,sigma_opp,sigma_opp,sigma,sigma]; %semisaturation constant
p.tau           = 50; %time constant (ms)
p.T             = 60000; %duration (ms)
p.I             = [c 0 0 c 0 0 0 0 0 0]; %input vector for dichoptic gratings
p.dt            = 5; %time step (ms) - for noise only
p.numSteps      = p.T/p.dt + 1; %number of steps
p.tol           = 1e-2; %tolerance to find zeros of FA-FB
p.duratLim      = 300; %minimum duration of a rivalry epoch (ms)
p.wtaLim        = 0.5; %minimum WTA index of a rivalry epoch
p.tauh          = 2000; % time constant of adaptation (ms)
p.wh            = 1; % weight of adaptation


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


%%% Cycles through parameter values %%%

n_runs = 3;
index = 1;

% Matrices of mean value of metrics for n_runs %
WTAmatrix       = zeros(50,50);
PercMatrix      = zeros(50,50);
DurMatrix       = zeros(50,50);
CVmatrix        = zeros(50,50);
DurMixMatrix    = zeros(50,50);
% Matrices of standard deviation of metrics over n_runs %
WTAsdMatrix     = zeros(50,50);
PercSDmatrix    = zeros(50,50);
DurSDmatrix     = zeros(50,50);
CVsdMatrix      = zeros(50,50);
DurMixSDmatrix  = zeros(50,50);

% cycle through noise intensities %
for ss = 0.005:0.005:0.25
    % cycle through input contrast %
    for cc = 0.02:0.02:1
        p.varNoise = ss;
        c = cc;
        p.I = [c 0 0 c 0 0 0 0 0 0];
        % calculate average value of metrics over n_runs %
        wta_runs    = zeros(1,n_runs);
        perc_runs   = zeros(1,n_runs);
        dur_runs    = zeros(1,n_runs);
        cv_runs     = zeros(1,n_runs);
        durmix_runs = zeros(1,n_runs);
        for repeat = 1:n_runs
            % simulation of 1 run %
            [WTA,PercRivalry,meanDur,CV,meanDurMix] = model_core(p,0,NoiseSwitch);
            wta_runs(repeat)    = WTA;
            perc_runs(repeat)   = PercRivalry;
            dur_runs(repeat)    = meanDur;
            cv_runs(repeat)     = CV;
            durmix_runs(repeat) = meanDurMix;
        end
        disp(index)
        % matrices of metrics %
        WTAmatrix(index)    = mean(wta_runs);
        PercMatrix(index)   = mean(perc_runs);
        DurMatrix(index)    = mean(dur_runs);
        CVmatrix(index)    = mean(cv_runs);
        DurMixMatrix(index)    = mean(durmix_runs);
        % matrices of standard deviations %
        WTAsdMatrix(index)  = std(wta_runs);
        PercSDmatrix(index) = std(perc_runs);
        DurSDmatrix(index)  = std(dur_runs);
        CVsdMatrix(index)  = std(cv_runs);
        DurMixSDmatrix(index)  = std(durmix_runs);
        index = index + 1;
    end
end

save('results.mat','WTAmatrix','PercMatrix','DurMatrix','CVmatrix','DurMixMatrix','WTAsdMatrix','PercSDmatrix','DurSDmatrix','CVsdMatrix','DurMixSDmatrix');

% to cycle through temporal correlation of OU noise, replace second cycle with:
%     for tt = 20:20:1000
% and p.I = [c 0 0 c 0 0 0 0 0 0]; with:
%     p.varImpResp = tt;



