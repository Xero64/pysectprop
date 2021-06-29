#%% Test Section

from IPython.display import display_markdown
from pysectprop.formed import CSection

#%% Create Formed C-Section
                 #hw, wuf, wlf,   ts, rm
csect = CSection(10.0, 6.0, 6.0, 1.4, 2.1)

display_markdown(csect)
ax = csect.plot()

#%% Mirror Section about Y Axis

csect.mirror_y()

display_markdown(csect)
ax = csect.plot()

#%% Mirror Section about Z Axis

csect.mirror_z()

display_markdown(csect)
ax = csect.plot()

#%% Mirror Section about Y Axis

csect.mirror_y()

display_markdown(csect)
ax = csect.plot()
