#%%
# Import Dependencies
from math import cos, sin, radians, acos, degrees, tan, sqrt
from matplotlib.pyplot import figure
from matplotlib.path import Path
from matplotlib.patches import PathPatch

#%%
# Specify two segments
angle = -72.0
length = 8.0
radius = 2.8

xa, ya = length*cos(radians(angle)), length*sin(radians(angle))
xb, yb = 0.0, 0.0
xc, yc = length, 0.0

x = [xa, xb, xc]
y = [ya, yb, yc]

#%%
# Plot Original
fig = figure(figsize=(12, 8))
ax = fig.gca()
ax.grid(True)
ax.set_aspect('equal')
p = ax.plot(x, y, '-o')

#%%
# Angle Between

dx1 = (xb-xa)
dy1 = (yb-ya)
dx2 = (xc-xb)
dy2 = (yc-yb)

l1 = (dx1**2+dy1**2)**0.5
l2 = (dx2**2+dy2**2)**0.5

dx1 = dx1/l1
dy1 = dy1/l1
dx2 = dx2/l2
dy2 = dy2/l2

ab = acos(-dx1*dx2-dy1*dy2)

lp = radius/tan(ab/2)

p1x = xb-dx1*lp
p1y = yb-dy1*lp

p2x = xb+dx2*lp
p2y = yb+dy2*lp

dxb = dx2-dx1
dyb = dy2-dy1

lb = (dxb**2+dyb**2)**0.5

dxb = dxb/lb
dyb = dyb/lb

lbc = radius/sin(ab/2)

xr = xb+dxb*lbc
yr = yb+dyb*lbc

fig = figure(figsize=(12, 8))
ax = fig.gca()
ax.grid(True)
ax.set_aspect('equal')
p = ax.plot(x, y, '-o')
p = ax.plot([p1x, xr, p2x], [p1y, yr, p2y])

#%%
# Check distance

rad1 = ((xr-p1x)**2+(yr-p1y)**2)**0.5
rad2 = ((xr-p2x)**2+(yr-p2y)**2)**0.5

print('ab = {:g}'.format(degrees(ab)))
print('rad1 = {:g}'.format(rad1))
print('rad2 = {:g}'.format(rad2))

#%%
# Calculate Intermediate Points

k = 4*(sqrt(2)-1)/3

q1x = p1x+lp*k*dx1
q1y = p1y+lp*k*dy1

q2x = p2x-lp*k*dx2
q2y = p2y-lp*k*dy2

#%%
# Plot Path

verts = [
    (xa, ya),
    (p1x, p1y),
    (q1x, q1y),
    (q2x, q2y),
    (p2x, p2y),
    (xc, yc)
]

codes = [Path.MOVETO, Path.LINETO, Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.LINETO]

path = Path(verts, codes)
patch = PathPatch(path, facecolor='none')

fig = figure(figsize=(12, 8))
ax = fig.gca()
ax.grid(True)
ax.set_aspect('equal')
p = ax.plot(x, y, '-o')
p = ax.add_patch(patch)
