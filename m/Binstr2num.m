function [result] = Binstr2num(binStr)
% 将char '0001' 转化为 [0 0 0 1]

len = length(binStr);
result = 2 * eyes(1, len);
for i = 1:len
    result(i) = str2double(binStr(i));
end
end

