#%%
# Import Dependencies
from IPython.display import display_markdown
from pysectprop.extruded import OmegaSection

#%%
# Create Section
omsect = OmegaSection(20.0, 1.6, 20.0, 1.6, 10.0, 1.6, ruf=1.4, rlf=2.8)
display_markdown(omsect)
ax = omsect.plot()

#%%
# Print to Standard Output
print(omsect)
