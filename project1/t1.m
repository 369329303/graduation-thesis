A = importdata('f3.txt');
x = A(:,1);
y = A(:,2);
z = A(:,3);

set(0,'defaultAxesFontSize', 22);
% subplot(1,2,1);
tri = delaunay(x,y);
trisurf(tri,x,y,z);
title('3d (adaptive-IDW.txt)');
xlabel('x/m');
ylabel('y/m');
zlabel('z/m');

% subplot(1,2,2);
% scatter(x, y, '.');
% title('2d (data.txt)');
% xlabel('x/m');
% ylabel('y/m');