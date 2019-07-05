A = importdata('source.txt');
x = A(:,1);
y = A(:,2);
z = A(:,3);

set(0,'defaultAxesFontSize', 22);
figure(1);
tri = delaunay(x,y);
trisurf(tri,x,y,z);
title('3d (source.txt)');
xlabel('x/m');
ylabel('y/m');
zlabel('z/m');

figure(2);
scatter(x, y, '.');
title('2d (source.txt)');
xlabel('x/m');
ylabel('y/m');