#%%
# Import Dependencies
from IPython.display import display_markdown
from pysectprop.standard import TubeSection
from pysectprop.standard import CircleSection
from pysectprop.general import HollowSection

#%%
# Create Tube Section
do = 80.0
di = 74.0

tube = TubeSection(do, di)
display_markdown(tube)
ax = tube.plot()

#%%
# Create Hollow Section
c1 = CircleSection(do)
c2 = CircleSection(di)

hollowsect = HollowSection(c1, c2, label='Round Tube')
display_markdown(hollowsect)
ax = hollowsect.plot()

#%%
# Translate Tube
yt = 15.0
zt = 25.0
tube.translate(yt, zt)
display_markdown(tube)
ax = tube.plot()

#%%
# Translate Hollow Section
yt = 15.0
zt = 25.0
hollowsect.translate(yt, zt)
display_markdown(hollowsect)
ax = hollowsect.plot()

