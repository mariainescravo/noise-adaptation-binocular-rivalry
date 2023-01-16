function [dom,mix,dur,init,fin,w] = analyseEpochs(Acell,Bcell,splits,segments,tSol,p)
% Checks length and WTA index of an epoch

dom  = 0;
mix  = 0;
dur  = 0;
init = 0;
fin  = 0;
w    = 0;

if ~isempty(Acell)
    t_init = mean([tSol(max([splits-1,1])),tSol(splits)]);
    t_fin  = mean([tSol(min([splits+segments,length(tSol)])),tSol(min([splits+segments-1,length(tSol)]))]);
    
    duration = t_fin - t_init;
    WTAepoch = WTAcalc(Acell,Bcell);
    
    %str_disp = sprintf("%d %.2f %.2f %d  %.2f%",splits,t_init,t_fin,round(duration),WTAepoch);
    %disp(str_disp)
    
    if (duration > p.duratLim)
        if (WTAepoch > p.wtaLim)
            dom = 1;
            %disp("|___ Dominant")
        else
            mix = 1;
            %disp("|___ Mixed")
        end
    end
    dur = duration;
    init = t_init;
    fin = t_fin;
    w = WTAepoch;
end