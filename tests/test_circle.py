from math import isclose, pi

from pysectprop.standard import CircleSection

d = 10.0

circle = CircleSection(d)

yt = 3.6
zt = 7.2
circle.translate(yt, zt)

def test_area():
    assert isclose(circle.A, pi*circle.d**2/4, abs_tol=1e-12)

def test_first_moment_of_area_in_y():
    assert isclose(circle.Ay, circle.A*yt, abs_tol=1e-12)

def test_first_moment_of_area_in_z():
    assert isclose(circle.Az, circle.A*zt, abs_tol=1e-12)

def test_centroid_y():
    assert isclose(circle.cy, yt, abs_tol=1e-12)

def test_centroid_z():
    assert isclose(circle.cz, zt, abs_tol=1e-12)

def test_moment_of_inertia_about_yy():
    assert isclose(circle.Iyy, circle.A*circle.d**2/16, abs_tol=1e-12)

def test_moment_of_inertia_about_zz():
    assert isclose(circle.Izz, circle.A*circle.d**2/16, abs_tol=1e-12)

def test_moment_of_inertia_about_yz():
    assert isclose(circle.Iyz, 0.0, abs_tol=1e-12)

def test_second_moment_of_area_about_yy():
    assert isclose(circle.Ayy, circle.Izz + circle.A*yt**2, abs_tol=1e-12)

def test_second_moment_of_area_about_zz():
    assert isclose(circle.Azz, circle.Iyy + circle.A*zt**2, abs_tol=1e-12)

def test_second_moment_of_area_about_yz():
    assert isclose(circle.Ayz, circle.A*yt*zt, abs_tol=1e-12)

print(f'circle.cos2thp = {circle.cos2thp}')
print(f'circle.sin2thp = {circle.sin2thp}')
print(f'circle.thp = {circle.thp}')

def test_principal_angle():
    assert isclose(circle.thp, 0.0, abs_tol=1e-12)

def test_principal_moments_of_inertia_in_y():
    assert isclose(circle.Iyp, circle.A*circle.d**2/16, abs_tol=1e-12)

def test_principal_moments_of_inertia_in_z():
    assert isclose(circle.Izp, circle.A*circle.d**2/16, abs_tol=1e-12)
