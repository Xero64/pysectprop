#%%
# Import Dependencies
from math import degrees

from IPython.display import display_markdown

from pysectprop.extruded import LSection

#%%
# Create Section
lsect1 = LSection(17.6, 1.6, 13.6, 1.6, 3.0)
display_markdown(lsect1)
ax = lsect1.plot()

display_markdown(lsect1.build_up_table)

#%%
# Create Section
lsect2 = LSection(lsect1.hw, lsect1.tw, lsect1.wf,
                  lsect1.tf, lsect1.rc)

yt = 300.0
zt = 450.0

lsect2.translate(yt, zt)
display_markdown(lsect2)
ax = lsect2.plot()

display_markdown(lsect2.build_up_table)

#%%
# Rotate Section
lsect1.rotate(degrees(-lsect1.thp))
display_markdown(lsect1)
ax = lsect1.plot()
