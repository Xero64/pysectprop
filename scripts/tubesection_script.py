#%%
# Import Dependencies
from IPython.display import display_markdown
from pysectprop.standard import TubeSection

#%%
# Create Section
do = 80.0
di = 74.0

tube = TubeSection(do, di)
display_markdown(tube)
ax = tube.plot()
