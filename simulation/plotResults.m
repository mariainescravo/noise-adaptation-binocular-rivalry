function plotResults(sPlot,p)
% Plots summation layer firing rates

FA              = sPlot.sol(:,19);
FB              = sPlot.sol(:,20);
tSol            = sPlot.time;
finalsplits     = sPlot.finalsplits;
WTA             = sPlot.WTA;
PercentRivalry  = sPlot.perc;
D               = sPlot.dur;
CV              = sPlot.CV;

figure("visible","on");
plot(tSol/1000,[FA FB],"Linewidth",3);
set(gcf, 'Position',  [0, 300, 2500, 800]);
ax = gca;
ax.FontSize = 26;
ax.FontWeight = "bold";
for i=1:length(finalsplits)
    xline(finalsplits(i)/1000,"k","Linewidth",1.5,"DisplayName","Significant Switches");
end
legend("Binocular A","Binocular B");
ylim([0 1]);
ylabel("Firing rate");
xlabel("Time (s)");
string_title = sprintf("WTA = %.2f, PDT = %d%%, D = %.2f s, CV = %.2f",WTA,round(PercentRivalry),D,CV);
title(string_title);

end

