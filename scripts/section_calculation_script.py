#%%
# Import Dependencies
from IPython.display import display_markdown

from pysectprop import MaterialSection
from pysectprop.formed import CSectionFormed
from pysectprop.general import Material
from pysectprop.results.sectionresult import SectionResult

#%%
# Create Section
csect = CSectionFormed(19.2, 13.6, 13.6, 1.6, 1.6, 'C Section (Formed)')

#%%
# Create Material
alum = Material(71000.0, label='Aluminium')
alum.set_yield_strengths(280.0, 260.0)
alum.set_ultimate_strengths(400.0, 380.0)

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
sf = 1.5
Fx_ult = -1500.0
My_ult = 20000.0
Mz_ult = 8000.0
Fx_lim = Fx_ult/sf
My_lim = My_ult/sf
Mz_lim = Mz_ult/sf

#%%
# Calculate Ultimate Section Axial Stresses
ultsectres = SectionResult(msect)
ultsectres.set_load(lc_ult, Fx_ult, My_ult, Mz_ult)
display_markdown(ultsectres)

#%%
# Calculate Limit Section Axial Stresses
limsectres = SectionResult(msect)
limsectres.set_load(lc_lim, Fx_lim, My_lim, Mz_lim, limit=True)
display_markdown(limsectres)
