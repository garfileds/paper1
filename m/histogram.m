% ��������
load rr1.txt
% ����ecdf��������xc���ľ���ֲ�����ֵf_ecdf
[f_ecdf, xc] = ecdf(rr1);
% �½�ͼ�δ��ڣ�Ȼ�����Ƶ��ֱ��ͼ��ֱ��ͼ��Ӧ7��С����
figure;
ecdfhist(f_ecdf, xc, 97);
hold on;
xlabel('IPI');  % ΪX��ӱ�ǩ
ylabel('Frequency');  % ΪY��ӱ�ǩ

% ����ksdensity�������к��ܶȹ���
% [f_ks1,xi1,u1] = ksdensity(rr);
% ���ƺ��ܶȹ���ͼ������������Ϊ��ɫʵ�ߣ��߿�Ϊ3
% plot(xi1,f_ks1,'r','linewidth',2)

xi1 = 900:1:1300;

ms = mean(rr1);  % ����x��ƽ��ֵ
ss = std(rr1);  % ����x�ı�׼��
% ����xi1������̬�ֲ��ܶȺ���ֵ����̬�ֲ��ľ�ֵΪms����׼��Ϊss
f_norm = normpdf(xi1,ms,ss); 
% ������̬�ֲ��ܶȺ���ͼ������������Ϊ��ɫ�㻮�ߣ��߿�Ϊ3
ax = plot(xi1,f_norm,'r','linewidth',2);
% set(handles, 'xtick', 800:200:1400);

% Ϊͼ�μӱ�ע�򣬱�ע���λ��������ϵ�����Ͻ�
% legend('Ƶ��ֱ��ͼ','���ܶȹ���ͼ', '��̬�ֲ��ܶ�ͼ', 'Location','NorthWest')