#%%
# Test Section

from IPython.display import display_markdown
from pysectprop.formed import LSection

#%%
# Create Formed L-Section

lsect = LSection(17.6, 13.4, 1.4, 3.0)

display_markdown(lsect)
ax = lsect.plot()

#%%
# Mirror Section about Y Axis

lsect.mirror_y()

display_markdown(lsect)
ax = lsect.plot()

#%%
# Mirror Section about Z Axis

lsect.mirror_z()

display_markdown(lsect)
ax = lsect.plot()

#%%
# Mirror Section about Y Axis

lsect.mirror_y()

display_markdown(lsect)
ax = lsect.plot()
