from math import isclose, sqrt

from pysectprop.general.line import Line
from pysectprop.general.point import Point

ya = 12.0
za = 5.0

yb = 7.0
zb = 10.0

pnta = Point(ya, za)
pntb = Point(yb, zb)

line = Line(pnta, pntb)

dy = pntb.y - pnta.y
dz = pntb.z - pnta.z
length = sqrt(dy**2 + dz**2)

def test_length():
    assert isclose(line.length, length, abs_tol=1e-12)

def test_area():
    assert isclose(line.A, (ya*zb - za*yb)/2, abs_tol=1e-12)

def test_first_moment_of_area_in_y():
    assert isclose(line.Ay, (ya*zb - za*yb)*(ya + yb)/6, abs_tol=1e-12)

def test_first_moment_of_area_in_z():
    assert isclose(line.Az, (ya*zb - za*yb)*(za + zb)/6, abs_tol=1e-12)

def test_second_moment_of_area_about_yy():
    assert isclose(line.Ayy, (ya**2 + ya*yb + yb**2)*(ya*zb - yb*za)/12, abs_tol=1e-12)

def test_second_moment_of_area_about_zz():
    assert isclose(line.Azz, (za**2 + za*zb + zb**2)*(ya*zb - yb*za)/12, abs_tol=1e-12)

def test_second_moment_of_area_about_yz():
    assert isclose(line.Ayz, (ya*zb + 2*ya*za + 2*yb*zb + yb*za)*(ya*zb - yb*za)/24,
                   abs_tol=1e-12)
