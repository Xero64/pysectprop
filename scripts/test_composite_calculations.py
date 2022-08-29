#%%
# Import Dependencies
from IPython.display import display_markdown
from pymaterial import metal_from_library
from pysectprop.extruded import LSection, RectangleSection
from pysectprop import MaterialSection, CompositeSection

#%%
# Create Section
lsect = LSection(17.6, 1.6, 13.6, 1.6, 3.0)
rsect = RectangleSection(17.6, 1.6)
rsect.translate(-0.8, 17.6/2)

#%%
# Create Aluminium Material
source = 'al2024t3sheet.json'
basis = 'A'
thickness = 1.6 # mm
alum = metal_from_library(source, basis, thickness)

#%%
# Create Aluminium Material
source = 'st15-5PHplate.json'
basis = 'S'
thickness = 12.0 # mm
ss = metal_from_library(source, basis, thickness)

#%%
# Create Material Section
mlsect = MaterialSection(lsect, alum)
mrsect = MaterialSection(rsect, ss)

display_markdown(mlsect)
display_markdown(mrsect)

#%%
# Create Composite Section
compsect = CompositeSection([mlsect, mrsect])

#%%
# Display Composite Section Output
display_markdown(compsect)

#%%
# Plot Composite Section
ax = compsect.plot()

#%%
# Loads
lc_ult = 'Ultimate Load Case'
lc_lim = 'Limit Load Case'
SF = 1.5
Fx_ult = -1500.0
My_ult = 20000.0
Mz_ult = 8000.0
Fx_lim = Fx_ult/SF
My_lim = My_ult/SF
Mz_lim = Mz_ult/SF

#%%
# Calculate Ultimate Section Axial Stresses
ultsectresults = compsect.apply_load(lc_ult, 'Ultimate', Fx_ult, My_ult, Mz_ult)
for ultsectresult in ultsectresults:
    display_markdown(ultsectresult)

#%%
# Calculate Limit Section Axial Stresses
limsectresults = compsect.apply_load(lc_lim, 'Limit', Fx_lim, My_lim, Mz_lim)
for limsectresult in limsectresults:
    display_markdown(limsectresult)
