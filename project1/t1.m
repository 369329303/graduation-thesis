A = importdata('sample.txt');
x = A(:,1);
y = A(:,2);
z = A(:,3);
tri = delaunay(x,y);
trisurf(tri,x,y,z);