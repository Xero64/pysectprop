#%%
# Test Section
from IPython.display import display_markdown

from pysectprop.formed import ZSectionFormed

#%%
# Create Formed L-Section
zsect = ZSectionFormed(17.6, 13.4, 13.4, 1.4, 3.0)

display_markdown(zsect)
ax = zsect.plot()

#%%
# Mirror Section about Y Axis
zsect.mirror_y()

display_markdown(zsect)
ax = zsect.plot()

#%%
# Mirror Section about Z Axis
zsect.mirror_z()

display_markdown(zsect)
ax = zsect.plot()

#%%
# Mirror Section about Y Axis
zsect.mirror_y()

display_markdown(zsect)
ax = zsect.plot()

#%%
# Thin-Walled Section
twsect = zsect.to_thin_walled_section()

display_markdown(twsect)
ax = twsect.plot()
