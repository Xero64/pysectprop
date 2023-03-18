#%%
# Test Section
from IPython.display import display_markdown
from pysectprop.formed import OmegaSectionFormed

#%%
# Create Formed C-Section
omsect = OmegaSectionFormed(10.0, 6.0, 10.0, 1.0, 3.0)

display_markdown(omsect)
ax = omsect.plot()

#%%
# Mirror Section about Y Axis
omsect.mirror_y()

display_markdown(omsect)
ax = omsect.plot()

#%%
# Mirror Section about Z Axis
omsect.mirror_z()

display_markdown(omsect)
ax = omsect.plot()

#%%
# Mirror Section about Y Axis
omsect.mirror_y()

display_markdown(omsect)
ax = omsect.plot()

#%%
# Thin-Walled Section
twsect = omsect.to_thin_walled_section()

display_markdown(twsect)
ax = twsect.plot()
