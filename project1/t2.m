A = importdata('sample.txt');
x = A(:,1);
y = A(:,2);
z = A(:,3);

[xq,yq] = meshgrid( min(x):10:max(x) , min(y):10:max(y));
zq = griddata(x,y,z,xq,yq);


mesh(xq,yq,zq);
hold on;
plot3(x,y,z,'o');
% xlim([-2.7 2.7])
% ylim([-2.7 2.7])