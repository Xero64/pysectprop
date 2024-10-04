from math import isclose, pi

from pysectprop.general import Material, MaterialSection
from pysectprop.standard import RectangleSection

Emod = 2.0
h = 5.0
b = 10.0
rect = RectangleSection(h, b)

yt = 3.6
zt = 7.2
rect.translate(yt, zt)

mat = Material(Emod)

matsect = MaterialSection(rect, mat)

if h > b:
    thp = 0.0
else:
    thp = pi/2

Ip1 = max(h**3*b/12, b**3*h/12)
Ip2 = min(b**3*h/12, h**3*b/12)

def test_area():
    assert isclose(matsect.EA, mat.E*rect.h*rect.b, abs_tol=1e-12)

def test_first_moment_of_area_in_y():
    assert isclose(matsect.EAy, mat.E*rect.A*yt, abs_tol=1e-12)

def test_first_moment_of_area_in_z():
    assert isclose(matsect.EAz, mat.E*rect.A*zt, abs_tol=1e-12)

def test_centroid_y():
    assert isclose(matsect.cy, yt, abs_tol=1e-12)

def test_centroid_z():
    assert isclose(matsect.cz, zt, abs_tol=1e-12)

def test_moment_of_inertia_about_yy():
    assert isclose(matsect.EIyy, mat.E*rect.h**3*rect.b/12, abs_tol=1e-12)

def test_moment_of_inertia_about_zz():
    assert isclose(matsect.EIzz, mat.E*rect.b**3*rect.h/12, abs_tol=1e-12)

def test_moment_of_inertia_about_yz():
    assert isclose(matsect.EIyz, 0.0, abs_tol=1e-12)

def test_second_moment_of_area_about_yy():
    assert isclose(matsect.EAzz, mat.E*(rect.Iyy + rect.A*zt**2), abs_tol=1e-12)

def test_second_moment_of_area_about_zz():
    assert isclose(matsect.EAyy, mat.E*(rect.Izz + rect.A*yt**2), abs_tol=1e-12)

def test_second_moment_of_area_about_yz():
    assert isclose(matsect.EAyz, mat.E*rect.A*yt*zt, abs_tol=1e-12)

def test_principal_angle():
    assert isclose(matsect.thp, thp, abs_tol=1e-12)

def test_principal_moment_of_inertia_in_y():
    assert isclose(matsect.EIyp, mat.E*Ip1, abs_tol=1e-12)

def test_principal_moment_of_inertia_in_z():
    assert isclose(matsect.EIzp, mat.E*Ip2, abs_tol=1e-12)
