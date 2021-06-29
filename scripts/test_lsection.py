#%% Test Section

from IPython.display import display_markdown
from pysectprop.extruded import LSection

lsect = LSection(17.6, 1.6, 13.4, 1.4, rc=0.0)

#%% Display Section Properties

display_markdown(lsect)

#%% Plot Section

ax = lsect.plot()
