#%%
# Import Dependencies
from IPython.display import display_markdown
from math import sin, cos, pi, degrees
from pysectprop.general import GeneralSection

#%%
# Properties of a Sector
yt = 0.0
zt = 0.0

al = pi/12
rad = 120.0
th = pi/6

A = th*rad**2
d = 2*rad*sin(th)/3/th
cy = yt + d*cos(al)
cz = zt + d*sin(al)
Ay = A*cy
Az = A*cz
thp = al - pi/2
Izp = rad**4/4*(th - 0.5*sin(2*th))
Iyp = rad**4/4*(th + 0.5*sin(2*th)) - 4*rad**4/9/th*sin(th)**2
Iyy = (Iyp + Izp)/2 + (Iyp - Izp)/2*cos(2*thp)
Izz = (Iyp + Izp)/2 - (Iyp - Izp)/2*cos(2*thp)
Iyz = (Iyp - Izp)/2*sin(2*al)
Ayy = Izz + A*cy**2
Azz = Iyy + A*cz**2
Ayz = Iyz + A*cy*cz

#%%
# Create Sector
y = [0.0, rad*cos(-th), rad*cos(0.0), rad*cos(th)]
z = [0.0, rad*sin(-th), rad*sin(0.0), rad*sin(th)]
r = [0.0, 0.0, rad, 0.0]
sector = GeneralSection(y, z, r, label='Sector')
sector.translate(yt, zt)
sector.rotate(degrees(al))

display_markdown(sector)
ax = sector.plot()

print(f'A = {A:.1f}')
print(f'Ay = {Ay:.0f}')
print(f'Az = {Az:.0f}')
print(f'cy = {cy:.1f}')
print(f'cz = {cz:.1f}')
print(f'Ayy = {Ayy:.0f}')
print(f'Azz = {Azz:.0f}')
print(f'Ayz = {Ayz:.0f}')
print(f'Iyy = {Iyy:.0f}')
print(f'Izz = {Izz:.0f}')
print(f'Iyz = {Iyz:.0f}')
print(f'thp = {degrees(thp):.1f}')
print(f'Iyp = {Iyp:.0f}')
print(f'Izp = {Izp:.0f}')

#%%
# Approximate Sector
num = 60000
thlst = [-th + i/num*2*th for i in range(num+1)]
y = [0.0] + [rad*cos(thi) for thi in thlst]
z = [0.0] + [rad*sin(thi) for thi in thlst]
r = [0.0] + [0.0 for _ in thlst]
approx = GeneralSection(y, z, r, label='Approx')
approx.translate(yt, zt)
approx.rotate(degrees(al))

display_markdown(approx)
ax = approx.plot()

print(f'A = {A:.1f}')
print(f'Ay = {Ay:.0f}')
print(f'Az = {Az:.0f}')
print(f'cy = {cy:.1f}')
print(f'cz = {cz:.1f}')
print(f'Ayy = {Ayy:.0f}')
print(f'Azz = {Azz:.0f}')
print(f'Ayz = {Ayz:.0f}')
print(f'Iyy = {Iyy:.0f}')
print(f'Izz = {Izz:.0f}')
print(f'Iyz = {Iyz:.0f}')
print(f'thp = {degrees(thp):.1f}')
print(f'Iyp = {Iyp:.0f}')
print(f'Izp = {Izp:.0f}')
