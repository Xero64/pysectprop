#%%
# Import Dependencies
from IPython.display import display_markdown
from pysectprop.extruded import LSection

#%%
# Create Section
lsect = LSection(17.6, 1.6, 13.4, 1.4, rc=0.8)
display_markdown(lsect)
ax = lsect.plot()

#%%
# Print to Standard Output
print(lsect)
