#%%
# Test Section
from IPython.display import display_markdown
from pysectprop.formed import CSectionFormed

#%%
# Create Formed C-Section
csect = CSectionFormed(10.0, 6.0, 6.0, 1.4, 2.1)

display_markdown(csect)
ax = csect.plot()

#%%
# Mirror Section about Y Axis
csect.mirror_y()

display_markdown(csect)
ax = csect.plot()

#%%
# Mirror Section about Z Axis
csect.mirror_z()

display_markdown(csect)
ax = csect.plot()

#%%
# Mirror Section about Y Axis
csect.mirror_y()

display_markdown(csect)
ax = csect.plot()

#%%
# Thin-Walled Section
twsect = csect.to_thin_walled_section()

display_markdown(twsect)
ax = twsect.plot()
