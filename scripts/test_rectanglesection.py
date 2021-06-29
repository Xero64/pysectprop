#%% Test Rectangle Section

from pysectprop.extruded import RectangleSection
from IPython.display import display_markdown

rectanglesect = RectangleSection(20, 10, rc = 0.0)

#%% Display Section Properties

display_markdown(rectanglesect)

#%% Plot Section

ax = rectanglesect.plot()
