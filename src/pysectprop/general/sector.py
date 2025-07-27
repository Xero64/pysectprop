from math import atan2, cos, degrees, isclose, pi, sin, sqrt
from typing import TYPE_CHECKING

from py2md.classes import MDTable

if TYPE_CHECKING:
    from .point import Point

class Sector():
    pnta: 'Point' = None
    pntb: 'Point' = None
    pntf: 'Point' = None
    _yaf: float = None
    _zaf: float = None
    _ybf: float = None
    _zbf: float = None
    _theta: float = None
    _radius: float = None
    _alpha: float = None
    _A: float = None
    _d: float = None
    _cy: float = None
    _cz: float = None
    _Ay: float = None
    _Az: float = None
    _thp: float = None
    _Iyp: float = None
    _Izp: float = None
    _Iav: float = None
    _Idf: float = None
    _cos2thp: float = None
    _sin2thp: float = None
    _Iyy: float = None
    _Izz: float = None
    _Iyz: float = None
    _Ayy: float = None
    _Azz: float = None
    _Ayz: float = None
    
    def __init__(self, pnta: 'Point', pntb: 'Point', pntf: 'Point') -> None:
        self.pnta = pnta
        self.pntb = pntb
        self.pntf = pntf
    
    @property
    def yaf(self) -> float:
        if self._yaf is None:
            self._yaf = self.pnta.y - self.pntf.y
        return self._yaf
    
    @property
    def zaf(self) -> float:
        if self._zaf is None:
            self._zaf = self.pnta.z - self.pntf.z
        return self._zaf
    
    @property
    def ybf(self) -> float:
        if self._ybf is None:
            self._ybf = self.pntb.y - self.pntf.y
        return self._ybf
    
    @property
    def zbf(self) -> float:
        if self._zbf is None:
            self._zbf = self.pntb.z - self.pntf.z
        return self._zbf
    
    @property
    def radius(self) -> float:
        if self._radius is None:
            self._radius = sqrt(self.yaf**2 + self.zaf**2)
            if not isclose(self._radius, sqrt(self.ybf**2 + self.zbf**2), rel_tol=1e-3):
                raise ValueError('The radius of the sector is not constant.')    
        return self._radius
    
    @property
    def theta(self) -> float:
        if self._theta is None:
            self._theta = atan2(self.yaf*self.zbf - self.zaf*self.ybf,
                                self.yaf*self.ybf + self.zaf*self.zbf)/2
        return self._theta
    
    @property
    def alpha(self) -> float:
        if self._alpha is None:
            self._alpha = atan2(self.zaf + self.zbf, self.yaf + self.ybf)
        return self._alpha
    
    @property
    def A(self) -> float:
        if self._A is None:
            self._A = self.theta*self.radius**2
        return self._A
    
    @property
    def d(self) -> float:
        if self._d is None:
            self._d = 2*self.radius*sin(self.theta)/3/self.theta
        return self._d        
    
    @property
    def cy(self) -> float:
        if self._cy is None:
            self._cy = self.pntf.y + self.d*cos(self.alpha)
        return self._cy

    @property
    def cz(self) -> float:
        if self._cz is None:
            self._cz = self.pntf.z + self.d*sin(self.alpha)
        return self._cz

    @property
    def Ay(self) -> float:
        if self._Ay is None:
            self._Ay = self.A*self.cy
        return self._Ay
    
    @property
    def Az(self) -> float:
        if self._Az is None:
            self._Az = self.A*self.cz
        return self._Az
    
    @property
    def thp(self) -> float:
        if self._thp is None:
            self._thp = self.alpha - pi/2
        return self._thp
    
    @property
    def Iyp(self) -> float:
        if self._Iyp is None:
            self._Iyp = self.radius**4/4*(self.theta + 0.5*sin(2*self.theta))
            self._Iyp -= 4*self.radius**4/9/self.theta*sin(self.theta)**2
        return self._Iyp
    
    @property
    def Izp(self) -> float:
        if self._Izp is None:
            self._Izp = self.radius**4/4*(self.theta - 0.5*sin(2*self.theta))
        return self._Izp
    
    @property
    def Iav(self) -> float:
        if self._Iav is None:
            self._Iav = (self.Iyp + self.Izp)/2
        return self._Iav
    
    @property
    def Idf(self) -> float:
        if self._Idf is None:
            self._Idf = (self.Iyp - self.Izp)/2
        return self._Idf
    
    @property
    def cos2thp(self) -> float:
        if self._cos2thp is None:
            self._cos2thp = cos(-2*self.thp)
        return self._cos2thp
    
    @property
    def sin2thp(self) -> float:
        if self._sin2thp is None:
            self._sin2thp = sin(-2*self.thp)
        return self._sin2thp
    
    @property
    def Iyy(self) -> float:
        if self._Iyy is None:
            self._Iyy = self.Iav + self.Idf*self.cos2thp
        return self._Iyy
    
    @property
    def Izz(self) -> float:
        if self._Izz is None:
            self._Izz = self.Iav - self.Idf*self.cos2thp
        return self._Izz
    
    @property
    def Iyz(self) -> float:
        if self._Iyz is None:
            self._Iyz = self.Idf*self.sin2thp
        return self._Iyz

    @property
    def Ayy(self) -> float:
        if self._Ayy is None:
            self._Ayy = self.Izz + self.A*self.cy**2
        return self._Ayy

    @property
    def Azz(self) -> float:
        if self._Azz is None:
            self._Azz = self.Iyy + self.A*self.cz**2
        return self._Azz

    @property
    def Ayz(self) -> float:
        if self._Ayz is None:
            self._Ayz = self.Iyz + self.A*self.cy*self.cz
        return self._Ayz
    
    def _repr_markdown_(self) -> str:
        mdstr = ''
        table = MDTable()
        table.add_column('pnta.y', '.3f', data=[self.pnta.y])
        table.add_column('pnta.z', '.3f', data=[self.pnta.z])
        table.add_column('pntb.y', '.3f', data=[self.pntb.y])
        table.add_column('pntb.z', '.3f', data=[self.pntb.z])
        table.add_column('pntf.y', '.3f', data=[self.pntf.y])
        table.add_column('pntf.z', '.3f', data=[self.pntf.z])
        mdstr += table._repr_markdown_()
        table = MDTable()
        table.add_column('radius', '.1f', data=[self.radius])
        table.add_column('theta', '.1f', data=[degrees(self.theta)])
        table.add_column('alpha', '.1f', data=[degrees(self.alpha)])
        table.add_column('d', '.1f', data=[self.d])
        table.add_column('cy', '.1f', data=[self.cy])
        table.add_column('cz', '.1f', data=[self.cz])
        mdstr += table._repr_markdown_()
        table = MDTable()
        table.add_column('A', '.1f', data=[self.A])
        table.add_column('Ay', '.0f', data=[self.Ay])
        table.add_column('Az', '.0f', data=[self.Az])
        table.add_column('thp', '.1f', data=[degrees(self.thp)])
        table.add_column('Iyp', '.0f', data=[self.Iyp])
        table.add_column('Izp', '.0f', data=[self.Izp])
        mdstr += table._repr_markdown_()
        table = MDTable()
        table.add_column('Iyy', '.0f', data=[self.Iyy])
        table.add_column('Izz', '.0f', data=[self.Izz])
        table.add_column('Iyz', '.0f', data=[self.Iyz])
        table.add_column('Ayy', '.0f', data=[self.Ayy])
        table.add_column('Azz', '.0f', data=[self.Azz])
        table.add_column('Ayz', '.0f', data=[self.Ayz])
        mdstr += table._repr_markdown_()
        return mdstr
    
    def __repr__(self) -> str:
        return f'<Sector {self.pnta}, {self.pntb}, {self.pntf}>'
    
    def __str__(self) -> str:
        return self.__repr__()
        