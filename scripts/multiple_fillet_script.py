#%%
# Import Dependencies
from math import degrees
from IPython.display import display_markdown
from pysectprop.general import GeneralSection
from pysectprop import config
config.l1frm = '.1f'
config.l2frm = '.2f'
config.l3frm = '.3f'
config.l4frm = '.4f'
config.angfrm = '.1f'

#%%
# Create Section
radius = 2.0
length = radius

y = [0.0, length, length, 2*length, 2*length, 0.0]
z = [0.0, 0.0, length, length, 2*length, 2*length]
r = [0.0, 0.0, radius, 0.0, 0.0, radius]

sect = GeneralSection(y, z, r)

# qcircle.translate(0.0, 4.0)

#%%
# Display Parameters
display_markdown(sect)

#%%
# Plot Multiple Fillet
ax = sect.plot()

#%%
# Check Path Objects
for obj in sect.path:
    print(obj)
    if hasattr(obj, 'pntf'):
        print(obj.pntf)
    if hasattr(obj, 'ang'):
        print(degrees(obj.ang))
