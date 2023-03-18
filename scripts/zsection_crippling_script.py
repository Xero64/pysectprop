#%%
# Import Dependencies
from IPython.display import display_markdown
from pysectprop.extruded import ZSection
from pysectprop.general import Material, MaterialSection, CripplingSection

#%%
# Create Section
zsect = ZSection(10, 1.6, 10, 1.6, 4.0, 1.3, rlf=1.2, ruf=1.6, label='Z Section')
display_markdown(zsect)
ax = zsect.plot()

#%%
# Create Material
alum = Material(71000.0, label='Aluminium')
alum.set_yield_strengths(280.0, 260.0)
alum.set_ultimate_strengths(400.0, 380.0)
display_markdown(alum)

#%%
# Create Material Section
msect = MaterialSection(zsect, alum)
display_markdown(msect)
ax = msect.plot()

#%%
# Thin Walled Section
twsect = zsect.to_thin_walled_section()
display_markdown(twsect)
ax = twsect.plot()

#%%
# Create Crippling Section
crsect = CripplingSection(twsect, alum, 0.32, 0.36)
display_markdown(crsect)

#%%
# Print Crippling Section Output
print(crsect)
