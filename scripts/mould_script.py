#%%
# Import Dependencies
from IPython.display import display_markdown
from pysectprop.general import Material, Mould

#%%
# Create Mould
mat  = Material(50000.0, 50000.0, label='Carbon Fabric')

y = [5.0, 0.0, 0.0, -5.0, -10.0]
z = [0.0, 0.0, 5.0, 5.0, 0.0]
r = [0.0, 0.5, 2.0, 2.0, 0.0]

mould = Mould(y, z, r, 'Mould Composite')
mould.add_ply('Ply 1', 0.25, 0.00, mat)
mould.add_ply('Ply 2', 0.25, 0.25, mat)
mould.add_ply('Ply 3', 0.25, 0.50, mat)
mould.add_ply('Ply 4', 0.25, 0.75, mat)
mould.add_ply('Ply 5', 0.25, 1.00, mat)
mould.add_ply('Ply 6', 0.25, 1.25, mat)

display_markdown(mould)
ax = mould.plot()
