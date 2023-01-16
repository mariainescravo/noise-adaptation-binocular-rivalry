function [WTA,PercentRivalry,meanD,coefVarD,meanDmix] = model_core_adap(p,PlotSwitch,GaussKernelSwitch)
% Simulation: ode45 integration, metrics calculation
%   Returns the WTA index, the percentage of dominance time (PDT),
%   the mean percept duration, the coefficient of variation (CV) of percept durations
%   and the mean mixed percept duration for one simulation run



% --- Calculation of noise --- %
if NoiseSwitch == 0
    % Ornstein-Uhlenbeck noise with Gaussian kernel
    p.N = createOrnsteinGaussKern(10,p);
elseif NoiseSwitch == 1
    % Ornstein-Uhlenbeck noise with exponential kernel
    p.N = createOrnsteinExpKern(10,p);
elseif NoiseSwitch == 2
    % White Gaussian noise
    p.N = createWhiteNoise(10,p);
elseif NoiseSwitch == 3
    % Pink 1/f noise
    p.N = createPinkNoise(10,p);
else
    fprintf("\nError setting up noise.\n");
end

% --- Integration using ODE45 --- %
Y0          = zeros(1,30);
tSpan       = [0 p.T];
[tSol,YSol] = ode45(@(t,X)evolDriveFiringAdap(t,X,p),tSpan,Y0);


FA      = YSol(:,19)';
FB      = YSol(:,20)';


% --- Calculate WTA index --- %

WTA = WTAcalc(FA,FB);

% --- Epochs --- %

V1  = FA-FB;
dominance = V1./abs(V1);

domChange = find(diff(dominance)~=0);
auxSplit  = [0 domChange length(dominance)];
segments = diff(auxSplit);

Aepochs = mat2cell(FA,1,segments);
Bepochs = mat2cell(FB,1,segments);

splits = auxSplit(1:end-1)+1;

% Select significant epochs to calculate PDT %

Csplits   = num2cell(splits);
Csegments = num2cell(segments);
[SigDom,SigMix,Dur,IniT,FinT,W] = cellfun(@(Acell,Bcell,splits,segments)analyseEpochs(Acell,Bcell,splits,segments,tSol,p),Aepochs,Bepochs,Csplits,Csegments,"UniformOutput",true);

ResEpo = [SigDom',SigMix',Dur',IniT',FinT',W'];

RivalryDuration = sum(ResEpo(ResEpo(:,1)~=0,3));
PercentRivalry = 100 * RivalryDuration/tSol(end);

% Calculate other metrics %

durations = ResEpo(ResEpo(:,1)~=0,3);
durations = durations ./ 1000;
meanD = mean(durations);
stdevD = std(durations);
coefVarD = meanD/stdevD;

mixdurations = ResEpo(ResEpo(:,2)~=0,3);
mixdurations = mixdurations ./ 1000;
meanDmix = mean(mixdurations);

% --- Plot --- %

if PlotSwitch == 1
    medsplits   = ResEpo(ResEpo(:,4)>5,4:5);
    finalsplits = ResEpo(ResEpo(:,1)~=0,4:5);

    sPlot.medsplits   = reshape(medsplits,1,[]);
    sPlot.finalsplits = reshape(finalsplits,1,[]);
    sPlot.WTA         = WTA;
    sPlot.perc        = PercentRivalry;
    sPlot.time        = tSol;
    sPlot.sol         = YSol;

    plotResults(sPlot,p);
end


end

