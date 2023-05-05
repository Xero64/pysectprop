#%%
# Test Rectangle Section
from pysectprop.standard import RectangleSection
from IPython.display import display_markdown

#%%
# Create Rectangle Section
rectanglesect = RectangleSection(20, 10, rc = 0.0)
display_markdown(rectanglesect)
ax = rectanglesect.plot()

#%%
# Rotate Section
rectanglesect.rotate(45.0)
display_markdown(rectanglesect)
ax = rectanglesect.plot()
