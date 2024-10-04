#%%
# Import Dependencies
from IPython.display import display_markdown
from pysectprop.standard import SquareSection

#%%
# Create Square Section
squaresect = SquareSection(10.0, rc = 2.0)
display_markdown(squaresect)
ax = squaresect.plot()

display_markdown(squaresect.build_up_table)

#%%
# Offset Square Section
yt = 1000.0
zt = 800.0
squaresect.translate(yt, zt)
display_markdown(squaresect)
ax = squaresect.plot()
