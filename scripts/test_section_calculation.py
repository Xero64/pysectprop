#%%
# Import Dependencies
from IPython.display import display_markdown
from pymaterial import metal_from_library
from pysectprop.formed import CSection
from pysectprop import MaterialSection
from pysectprop.results.materialsectionresult import SectionResult

#%%
# Create Section
csect = CSection(19.2, 13.6, 13.6, 1.6, 1.6)

#%%
# Create Material
source = 'al2024t3sheet.json'
basis = 'A'
thickness = 1.6 # mm
alum = metal_from_library(source, basis, thickness)

#%%
# Create Material Section
msect = MaterialSection(csect, alum)
display_markdown(msect)

#%%
# Plot Material Section
ax = msect.plot()

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
ultsectres = SectionResult(msect)
ultsectres.apply_load(lc_ult, 'Ultimate', Fx_ult, My_ult, Mz_ult)
display_markdown(ultsectres)

#%%
# Calculate Limit Section Axial Stresses
limsectres = SectionResult(msect)
limsectres.apply_load(lc_lim, 'Limit', Fx_lim, My_lim, Mz_lim)
display_markdown(limsectres)
