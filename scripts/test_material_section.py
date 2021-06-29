#%% Import Dependencies
from IPython.display import display_markdown
from pymaterial import metal_from_library
from pysectprop.extruded import LSection
from pysectprop import MaterialSection

#%% Create Section
lsect = LSection(17.6, 1.6, 13.6, 1.6, 3.0)

#%% Create Material
source = 'al2024t3sheet.json'
basis = 'A'
thickness = 1.6 # mm
alum = metal_from_library(source, basis, thickness)

#%% Create Material Section
msect = MaterialSection(lsect, alum)

#%% Display Material Output
display_markdown(alum)

#%% Display Section Output
display_markdown(lsect)

#%% Display Material Section Output
display_markdown(msect)

#%% Plot Material Section
ax = msect.plot()
