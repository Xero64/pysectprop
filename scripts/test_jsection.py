#%% Test Section

from IPython.display import display_markdown
from pysectprop.extruded import JSection

# Inputs to JSection (web height, web thickness, width upper flange, thickness upper flange,
#                     width lower flange, thickness lower flange, optional height lip,
#                     optional thickness lip )
jsect = JSection(10, 1.6, 10, 1.6, 4.0, 1.3)
#%% Display Section Properties

display_markdown(jsect)

#%% Plot Section

ax = jsect.plot()
