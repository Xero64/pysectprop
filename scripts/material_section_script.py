#%%
# Import Dependencies
from IPython.display import display_markdown
from pysectprop.general import Material
from pysectprop.extruded import LSection
from pysectprop import MaterialSection

#%%
# Create Section
lsect = LSection(17.6, 1.6, 13.6, 1.6, 3.0, label='Extrusion')
display_markdown(lsect)

#%%
# Create Material
alum = Material(71000.0, label='Aluminium')
alum.set_yield_strengths(280.0, 260.0)
alum.set_ultimate_strengths(400.0, 380.0)
display_markdown(alum)

#%%
# Create Material Section
msect = MaterialSection(lsect, alum)
display_markdown(msect)
ax = msect.plot()
