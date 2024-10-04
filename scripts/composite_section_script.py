#%%
# Import Dependencies
from IPython.display import display_markdown
from pysectprop import CompositeSection, MaterialSection
from pysectprop.extruded import LSection
from pysectprop.general import Material
from pysectprop.standard import RectangleSection

#%%
# Create Section
lsect = LSection(17.6, 1.6, 13.6, 1.6, 3.0, label='L Section')
rsect = RectangleSection(17.6, 1.6, label='Rectangle Section')
rsect.translate(-0.8, 17.6/2)

#%%
# Create Aluminium Material

#%%
# Create Aluminium Material
alum = Material(71000.0, label='Aluminium')
alum.set_yield_strengths(280.0, 260.0)
alum.set_ultimate_strengths(400.0, 380.0)

#%%
# Create Steel Material
steel = Material(200000.0, label='Steel')
steel.set_yield_strengths(1000.0, 960.0)
steel.set_ultimate_strengths(1200.0, 1160.0)

#%%
# Create Material Section
mlsect = MaterialSection(lsect, alum)
mrsect = MaterialSection(rsect, steel)

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
