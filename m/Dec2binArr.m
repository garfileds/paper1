function [result] = Dec2binArr(decNum, size)
% ��char '0001' ת��Ϊ [0 0 0 1]

decNum = dec2bin(decNum, size);
len = length(decNum);
result = 2 * ones(1, len);
for i = 1:len
    result(i) = str2double(decNum(i));
end
end

