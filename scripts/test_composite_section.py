#%% Import Dependencies
from IPython.display import display_markdown
from pymaterial import metal_from_library
from pysectprop.extruded import LSection, RectangleSection
from pysectprop import MaterialSection, CompositeSection

#%% Create Section
lsect = LSection(17.6, 1.6, 13.6, 1.6, 3.0)
rsect = RectangleSection(17.6, 1.6)
rsect.translate(-0.8, 17.6/2)

#%% Create Aluminium Material
source = 'al2024t3sheet.json'
basis = 'A'
thickness = 1.6 # mm
alum = metal_from_library(source, basis, thickness)

#%% Create Aluminium Material
source = 'st15-5PHplate.json'
basis = 'S'
thickness = 12.0 # mm
ss = metal_from_library(source, basis, thickness)

#%% Create Material Section
mlsect = MaterialSection(lsect, alum)
mrsect = MaterialSection(rsect, ss)

display_markdown(mlsect)
display_markdown(mrsect)

#%% Create Composite Section
compsect = CompositeSection([mlsect, mrsect])

#%% Display Composite Section Output
display_markdown(compsect)

#%% Plot Composite Section
ax = compsect.plot()
