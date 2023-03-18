#%%
# Import Dependencies
from math import sqrt
from matplotlib.pyplot import figure
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Circle

#%%
# Plot Path
path_data = [
    (Path.MOVETO, (1.58, -2.57)),
    (Path.CURVE4, (0.35, -1.1)),
    (Path.CURVE4, (-1.75, 2.0)),
    (Path.CURVE4, (0.375, 2.0)),
    (Path.LINETO, (0.85, 1.15)),
    (Path.CURVE4, (2.2, 3.2)),
    (Path.CURVE4, (3, 0.05)),
    (Path.CURVE4, (2.0, -0.5)),
    (Path.CLOSEPOLY, (1.58, -2.57)),
    ]

codes, verts = zip(*path_data)

path = Path(verts, codes)
patch = PathPatch(path, facecolor='r', alpha=0.5)

fig = figure(figsize=(12, 8))
ax = fig.gca()
ax.add_patch(patch)
ax.grid()
ax.axis('equal')

#%%
# Display Values

print(codes)
print(verts)

#%%
# Test Circle

# angle = radians(30.0)
# length = tan(angle)

length = 0.5522847498

print(length)

length = 4*(sqrt(2)-1)/3

print(length)

verts = [
    (1.0, 0.0),
    (1.0, length),
    (length, 1.0),
    (0.0, 1.0),
    (-length, 1.0),
    (-1.0, length),
    (-1.0, 0.0),
    (-1.0, -length),
    (-length, -1.0),
    (0.0, -1.0),
    (length, -1.0),
    (1.0, -length),
    (1.0, 0.0)
]

codes = [1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]

circle = Circle((0.0, 0.0), radius=1.0, alpha=0.3)

path = Path(verts, codes)
patch = PathPatch(path, facecolor='r', alpha=0.5)

fig = figure(figsize=(12, 8))
ax = fig.gca()
ax.add_patch(circle)
ax.add_patch(patch)
ax.grid()
ax.axis('equal')

x = []
y = []
for vert in verts:
    x.append(vert[0])
    y.append(vert[1])

ax.plot(x, y)

#%%
# Clip Path
scale = 0.5

scaleverts = []
for vert in verts:
    scaleverts.append((scale*vert[0], scale*vert[1]))

scalepath = Path(scaleverts, codes)
scalepatch = PathPatch(scalepath)

path = Path(verts, codes)
patch = PathPatch(path, facecolor='r', alpha=0.5)
patch.set_clip_path(scalepatch)
patch.set_clip_on(True)

fig = figure(figsize=(12, 8))
ax = fig.gca()
ax.add_patch(patch)
# ax.add_patch(scalepatch)
ax.grid()
ax.axis('equal')

#%%
# Plot Scale Patch
fig = figure(figsize=(12, 8))
ax = fig.gca()
# ax.add_patch(patch)
ax.add_patch(scalepatch)
ax.grid()
ax.axis('equal')
