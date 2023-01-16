function dXdt = evolDriveFiringAdap(t,X,p)
% System of 30 differential equations to integrate
%   10 types of neurons with drive equations (synaptic integration), 
%   firing rate equations and adaptation equations; 
%   interpolation of noise
D = X(1:10);
F = X(11:20);
H = X(21:30);
auxVec  = [-F(5)-F(6),-F(5)-F(6),-F(7)-F(8),-F(7)-F(8),F(3)-F(1),F(4)-F(2),F(1)-F(3),F(2)-F(4),F(1)+F(3),F(2)+F(4)];
poolM   = [D(1),D(2),D(3),D(4)];
poolORL = [D(5),D(6),0,0];
poolOLR = [D(7),D(8),0,0];
poolS   = [D(9),D(10),0,0];
pool    = [poolM;poolM;poolM;poolM;poolORL;poolORL;poolOLR;poolOLR;poolS;poolS];
dDdt = zeros(10,1);
dFdt = zeros(10,1);
dHdt = zeros(10,1);

N = interp1(0:p.dt:p.T,(p.N)',t);
N = N';

for i = 1:10
   dDdt(i) = (-D(i) + p.I(i) + auxVec(i) + N(i,:))/p.tau;
   dFdt(i) = (-F(i) + rectify(D(i))/sum(rectify([p.s(i) sqrt(H(i)) pool(i,:)])))/p.tau;
   dHdt(i) = (-H(i) + p.wh * F(i))/p.tauh;
   if i > 4 && i < 9
       dHdt(i) = 0;
   end
end
dXdt = [dDdt;dFdt;dHdt];
end 

% to simulate the system with subtractive adaptation, replace lines 23 and 25 with:
%  dDdt(i) = (-D(i) + p.I(i) + auxVec(i) + N(i,:) - H(i))/p.tau;
%  dHdt(i) = (-H(i) + F(i))/p.tauh;
% to simulate the system without adaptation, replace line 25 with:
%  dHdt(i) = 0;