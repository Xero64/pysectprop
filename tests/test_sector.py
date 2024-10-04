from math import cos, isclose, pi, sin

from pysectprop.general.point import Point
from pysectprop.general.sector import Sector

yt = 300.0
zt = 450.0

al = pi/12
rad = 120.0
th = pi/6

area = th*rad**2
d = 2*rad*sin(th)/3/th
cy = yt + d*cos(al)
cz = zt + d*sin(al)
Ay = area*cy
Az = area*cz
thp = al - pi/2
Izp = rad**4/4*(th - 0.5*sin(2*th))
Iyp = rad**4/4*(th + 0.5*sin(2*th)) - 4*rad**4/9/th*sin(th)**2
Iyy = (Iyp + Izp)/2 + (Iyp - Izp)/2*cos(-2*thp)
Izz = (Iyp + Izp)/2 - (Iyp - Izp)/2*cos(-2*thp)
Iyz = (Iyp - Izp)/2*sin(-2*thp)
Ayy = Izz + area*cy**2
Azz = Iyy + area*cz**2
Ayz = Iyz + area*cy*cz

pnta = Point(yt + rad*cos(-th+al), zt + rad*sin(-th+al))
pntb = Point(yt + rad*cos(th+al), zt + rad*sin(th+al))
pntf = Point(yt, zt)

sector = Sector(pnta, pntb, pntf)

def test_area():
    assert isclose(sector.A, area, abs_tol=1e-12)

def test_first_moment_of_area_in_y():
    assert isclose(sector.Ay, Ay, abs_tol=1e-12)

def test_first_moment_of_area_in_z():
    assert isclose(sector.Az, Az, abs_tol=1e-12)

def test_centroid_y():
    assert isclose(sector.cy, cy, abs_tol=1e-12)

def test_centroid_z():
    assert isclose(sector.cz, cz, abs_tol=1e-12)

def test_moment_of_inertia_about_yy():
    assert isclose(sector.Iyy, Iyy, abs_tol=1e-12)

def test_moment_of_inertia_about_zz():
    assert isclose(sector.Izz, Izz, abs_tol=1e-12)

def test_moment_of_inertia_about_yz():
    assert isclose(sector.Iyz, Iyz, abs_tol=1e-12)

def test_second_moment_of_area_about_yy():
    assert isclose(sector.Ayy, Ayy, abs_tol=1e-12)

def test_second_moment_of_area_about_zz():
    assert isclose(sector.Azz, Azz, abs_tol=1e-12)

def test_second_moment_of_area_about_yz():
    assert isclose(sector.Ayz, Ayz, abs_tol=1e-12)
    