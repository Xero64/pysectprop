#%%
# Import Dependencies
from IPython.display import display_markdown
from pysectprop.extruded import JSection

#%%
# Create Section
jsect = JSection(10, 1.6, 10, 1.6, 4.0, 1.3, rlf=1.2, ruf=1.6)
display_markdown(jsect)
ax = jsect.plot()

#%%
# Print to Standard Output
print(jsect)
