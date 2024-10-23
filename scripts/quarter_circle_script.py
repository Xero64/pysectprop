#%%
# Import Dependencies

from math import pi

from IPython.display import display_markdown

from pysectprop import GeneralSection, config

config.l1frm = '.1f'
config.l2frm = '.2f'
config.l3frm = '.3f'
config.l4frm = '.4f'
config.angfrm = '.1f'

#%%
# Create Section

radius = 2.0
length = radius

y = [0.0, radius, radius, 0.0]
z = [0.0, 0.0, radius, radius]
r = [0.0, 0.0, radius, 0.0]

qcircle1 = GeneralSection(y, z, r)

# qcircle.translate(0.0, 4.0)

#%%
# Display Parameters

display_markdown(qcircle1)

# https://en.wikipedia.org/wiki/List_of_second_moments_of_area

A = pi*radius**2/4
cy = 4*radius/3/pi
Ay = A*cy
cz = 4*radius/3/pi
Az = A*cz
Iyy = (pi/16-4/9/pi)*radius**4
Izz = (pi/16-4/9/pi)*radius**4

print('A = {:}'.format(A))
print('Ay = {:}'.format(Ay))
print('Az = {:}'.format(Az))
print('cy = {:}'.format(cy))
print('cz = {:}'.format(cz))
print('Iyy = {:}'.format(Iyy))
print('Izz = {:}'.format(Izz))

#%%
# Plot Circle

ax = qcircle1.plot()
# ax.set_xlim(-4.0, 2.0)

#%%
# Circle Path

# from math import degrees

for obj in qcircle1.path:
    print(obj)
    if hasattr(obj, 'pntf'):
        print(obj.pntf)

#%%
# Display Build-Up
display_markdown(qcircle1.build_up_table)

#%%
# Quarter Circle 2

y2 = [0.0, 0.0, -radius, -radius]
z2 = [0.0, radius, radius, 0.0]
r2 = [0.0, 0.0, radius, 0.0]

qcircle2 = GeneralSection(y2, z2, r2)

ax = qcircle2.plot()

display_markdown(qcircle2)

display_markdown(qcircle2.build_up_table)

#%%
# Quarter Circle 3

y3 = [0.0, -radius, -radius, 0.0]
z3 = [0.0, 0.0, -radius, -radius]
r3 = [0.0, 0.0, radius, 0.0]

qcircle3 = GeneralSection(y3, z3, r3)

ax = qcircle3.plot()

display_markdown(qcircle3)

display_markdown(qcircle3.build_up_table)

#%%
# Quarter Circle 4

y4 = [0.0, 0.0, radius, radius]
z4 = [0.0, -radius, -radius, 0.0]
r4 = [0.0, 0.0, radius, 0.0]

qcircle4 = GeneralSection(y4, z4, r4)

ax = qcircle4.plot()

display_markdown(qcircle4)

display_markdown(qcircle4.build_up_table)
