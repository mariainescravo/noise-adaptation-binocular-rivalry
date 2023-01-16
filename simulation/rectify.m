function res = rectify(vect)
% Halfwave rectification
res = max(vect,0).^2;
end