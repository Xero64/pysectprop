#%%
# Import Dependencies
from IPython.display import display_markdown

from pysectprop.extruded import ISection

#%%
# Create Section
isect = ISection(20.0, 1.6, 15.0, 1.4, 10.0, 1.2, rlf=1.2, ruf=1.6)
display_markdown(isect)
ax = isect.plot()

#%%
# Print to Standard Output
print(isect)
