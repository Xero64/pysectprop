#%%
# Hollow Path
from matplotlib.pyplot import figure
from matplotlib.path import Path
from matplotlib.patches import PathPatch

def reverse_simple_path(path: Path):
    vertices = path.vertices.copy()
    codes = path.codes.copy()
    vertices[1:-2] = path.vertices[-3:0:-1]
    codes[1:-1] = path.codes[-2:0:-1]
    return Path(vertices, codes, readonly=path.readonly)

def make_donut(center, outer, inner):
    p1 = Path.circle(center, outer)
    p2 = reverse_simple_path(Path.circle(center, inner))
    return PathPatch(Path.make_compound_path(p1, p2))

fig = figure(figsize=(12, 8))
ax = fig.gca()
ax.plot([0, 400], [0, 300], 'r')
ax.add_patch(make_donut((200, 150), 100, 75))
ax.grid()
ax.axis('equal')
