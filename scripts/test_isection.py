#%% Test Section

from IPython.display import display_markdown
from pysectprop.extruded import ISection
isect = ISection(20.0, 1.6, 15.0, 1.4, 10.0, 1.2, r1=1.2, r2=1.6)

#%% Display Section Properties

display_markdown(isect)

#%% Plot Section

ax = isect.plot()
# ax = isect.plot_arc_control(ax=ax)
