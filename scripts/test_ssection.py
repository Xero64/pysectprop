#%% Test SSection

from pysectprop.extruded import SSection
from IPython.display import display_markdown

# 10 Inputs for 2 lips & 8 Inputs for 1 (leave out tl2 and hl2)
# (hw, tw, wf1, tf1, wf2, tf2, tl1, hl1, tl2, hl2):

ssect = SSection(30.0, 1.6, 20.0, 1.6, 15.0, 2.0, 2.0, 5.0, 1.0, 3.5)
# ssect = SSection(30.0, 1.6, 20.0, 1.6, 15.0, 2.0, 2.0, 5.0)

#%% Section Properties

display_markdown(ssect)
ax = ssect.plot()

#%% Mirror Section about YY

ssect.mirror_y()
display_markdown(ssect)
ax = ssect.plot()

#%% Mirror Section about ZZ

ssect.mirror_z()
display_markdown(ssect)
ax = ssect.plot()
