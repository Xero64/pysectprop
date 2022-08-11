#%%
# Import Dependencies
from IPython.display import display_markdown
from pysectprop.extruded import TSection

#%%
# Create T-Section
tsect = TSection(32, 1.6, 38, 1.6, 1.0)
display_markdown(tsect)

#%%
# Plot Section
ax = tsect.plot()
