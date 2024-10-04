from math import isclose, pi

from pysectprop.standard import RectangleSection

h = 5.0
b = 10.0
rect = RectangleSection(h, b)

yt = 3.6
zt = 7.2
rect.translate(yt, zt)

if h > b:
    thp = 0.0
else:
    thp = pi/2

Ip1 = max(h**3*b/12, b**3*h/12)
Ip2 = min(b**3*h/12, h**3*b/12)

def test_area():
    assert isclose(rect.A, rect.h*rect.b, abs_tol=1e-12)

def test_first_moment_of_area_in_y():
    assert isclose(rect.Ay, rect.A*yt, abs_tol=1e-12)

def test_first_moment_of_area_in_z():
    assert isclose(rect.Az, rect.A*zt, abs_tol=1e-12)

def test_centroid_y():
    assert isclose(rect.cy, yt, abs_tol=1e-12)

def test_centroid_z():
    assert isclose(rect.cz, zt, abs_tol=1e-12)

def test_moment_of_inertia_about_yy():
    assert isclose(rect.Iyy, rect.h**3*rect.b/12, abs_tol=1e-12)

def test_moment_of_inertia_about_zz():
    assert isclose(rect.Izz, rect.b**3*rect.h/12, abs_tol=1e-12)

def test_moment_of_inertia_about_yz():
    assert isclose(rect.Iyz, 0.0, abs_tol=1e-12)

def test_second_moment_of_area_about_yy():
    assert isclose(rect.Azz, rect.Iyy + rect.A*zt**2, abs_tol=1e-12)

def test_second_moment_of_area_about_zz():
    assert isclose(rect.Ayy, rect.Izz + rect.A*yt**2, abs_tol=1e-12)

def test_second_moment_of_area_about_yz():
    assert isclose(rect.Ayz, rect.A*yt*zt, abs_tol=1e-12)

def test_principal_angle():
    assert isclose(rect.thp, thp, abs_tol=1e-12)

def test_principal_moment_of_inertia_in_y():
    assert isclose(rect.Iyp, Ip1, abs_tol=1e-12)

def test_principal_moment_of_inertia_in_z():
    assert isclose(rect.Izp, Ip2, abs_tol=1e-12)
