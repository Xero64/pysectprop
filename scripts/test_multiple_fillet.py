#%%
# Import Dependencies

from IPython.display import display_markdown, HTML
from pysectprop import set_format
from pysectprop import GeneralPolygon
from math import pi

set_format(l1frm='{:.12f}', l2frm='{:.12f}', l3frm='{:.12f}', l4frm='{:.12f}')

#%%
# Create Section

radius = 2.0
length = radius

y = [0.0, length, length, 2*length, 2*length, 0.0]
z = [0.0, 0.0, length, length, 2*length, 2*length]
r = [0.0, 0.0, radius, 0.0, 0.0, radius]

sect = GeneralPolygon(y, z, r)

# qcircle.translate(0.0, 4.0)

#%%
# Display Parameters

display_markdown(sect)

#%%
# Plot Multiple Fillet

ax = sect.plot()

#%%
# Check Path Objects

from math import degrees

for obj in sect.path:
    print(obj)
    if hasattr(obj, 'pntf'):
        print(obj.pntf)
    if hasattr(obj, 'ang'):
        print(degrees(obj.ang))
