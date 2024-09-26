#%%
# Import Dependencies
from IPython.display import display_markdown
from pysectprop import GeneralSection
from pysectprop import config

config.l1frm = '.1f'
config.l2frm = '.4f'
config.l3frm = '.3f'
config.l4frm = '.4f'
config.angfrm = '.4f'

#%%
# Create Section
radius = 2.0
length = radius

y = [length, -length, -length, length]
z = [length, length, -length, -length]
r = [radius, radius, radius, radius]

circle = GeneralSection(y, z, r)

# yt = 3.6
# zt = 7.2
# circle.translate(yt, zt)

#%%
# Display Parameters
display_markdown(circle)

# A = pi*radius**2
# Ay = A*yt
# Az = A*zt

# Iyy = pi*radius**4/4
# Izz = pi*radius**4/4

# print('A = {:g} mm**2'.format(A))
# print('Ay = {:g} mm**3'.format(Ay))
# print('Az = {:g} mm**3'.format(Az))
# print('Iyy = {:g} mm**4'.format(Iyy))
# print('Izz = {:g} mm**4'.format(Izz))

#%%
# Plot Circle
ax = circle.plot()

#%%
# Display Build-Up
display_markdown(circle.build_up_table)
