function [result] = Binstr2num(binStr)
% ��char '0001' ת��Ϊ [0 0 0 1]

len = length(binStr);
result = 2 * eyes(1, len);
for i = 1:len
    result(i) = str2double(binStr(i));
end
end

