from typing import List, Tuple, Optional
from math import atan2, sqrt
from py2md.classes import MDTable
from .point import Point
from .. import config

K = 1.0 - 4.0*(2.0**0.5 - 1.0)/3.0

class Arc():
    pnta: Point = None
    pntb: Point = None
    pntc: Point = None
    pntd: Point = None
    pnte: Point = None
    pntf: Point = None
    sinang: float = None
    cosang: float = None
    ang: float = None
    sango2: float = None
    radius: float = None
    sinphi: float = None
    cosphi: float = None
    _A: float = None
    _Ay: float = None
    _Az: float = None
    _Ayy: float = None
    _Azz: float = None
    _Ayz: float = None
    _A_seg: float = None
    _Ay_seg: float = None
    _Az_seg: float = None
    _Ayy_seg: float = None
    _Azz_seg: float = None
    _Ayz_seg: float = None
    _A_line: float = None
    _Ay_line: float = None
    _Az_line: float = None
    _Ayy_line: float = None
    _Azz_line: float = None
    _Ayz_line: float = None
    def __init__(self, pnta: Point, pntb: Point, pntc: Point, pntf: Point) -> None:
        self.pnta = pnta
        self.pntb = pntb
        self.pntc = pntc
        self.pntf = pntf
        self.update()
    def update(self) -> None:
        dy = self.pntb.y - self.pnta.y
        dz = self.pntb.z - self.pnta.z
        length = sqrt(dy**2 + dz**2)
        dy1 = self.pnta.y - self.pntc.y
        dz1 = self.pnta.z - self.pntc.z
        dy2 = self.pntb.y - self.pntc.y
        dz2 = self.pntb.z - self.pntc.z
        yd = self.pntc.y + dy1*K
        zd = self.pntc.z + dz1*K
        ye = self.pntc.y + dy2*K
        ze = self.pntc.z + dz2*K
        self.pntd = Point(yd, zd)
        self.pnte = Point(ye, ze)
        l1 = sqrt(dy1**2 + dz1**2)
        dy3 = self.pnta.y - self.pntf.y
        dz3 = self.pnta.z - self.pntf.z
        dy4 = self.pntb.y - self.pntf.y
        dz4 = self.pntb.z - self.pntf.z
        l3 = sqrt(dy3**2 + dz3**2)
        l4 = sqrt(dy4**2 + dz4**2)
        self.sinang = (dy3*dz4 - dz3*dy4)/l3/l4
        self.cosang = (dy3*dy4 + dz3*dz4)/l3/l4
        self.ang = atan2(self.sinang, self.cosang)
        self.sango2 = (dy*dz1 - dz*dy1)/length/l1
        yaf = self.pnta.y - self.pntf.y
        zaf = self.pnta.z - self.pntf.z
        self.radius = sqrt(yaf**2 + zaf**2)
        zcf = self.pntc.z - self.pntf.z
        ycf = self.pntc.y - self.pntf.y
        lcf = sqrt(ycf**2 + zcf**2)
        self.sinphi = zcf/lcf
        self.cosphi = ycf/lcf
    @property
    def A_seg(self) -> float:
        if self._A_seg is None:
            rad = self.radius
            ang = self.ang
            sinang = self.sinang
            self._A_seg = rad**2/2*(ang-sinang)
        return self._A_seg
    @property
    def A_line(self) -> float:
        if self._A_line is None:
            ya = self.pnta.y
            za = self.pnta.z
            yb = self.pntb.y
            zb = self.pntb.z
            self._A_line = (ya*zb-za*yb)/2
        return self._A_line
    @property
    def A(self) -> float:
        if self._A is None:
            self._A = self.A_seg + self.A_line
        return self._A
    @property
    def Ay_seg(self) -> float:
        if self._Ay_seg is None:
            yf = self.pntf.y
            rad = self.radius
            sango2 = self.sango2
            cosphi = self.cosphi
            self._Ay_seg = 2/3*rad**3*sango2**3*cosphi+self.A_seg*yf
        return self._Ay_seg
    @property
    def Ay_line(self) -> float:
        if self._Ay_line is None:
            ya = self.pnta.y
            za = self.pnta.z
            yb = self.pntb.y
            zb = self.pntb.z
            self._Ay_line = (ya*zb-za*yb)*(ya+yb)/6
        return self._Ay_line
    @property
    def Ay(self) -> float:
        if self._Ay is None:
            self._Ay = self.Ay_seg+self.Ay_line
        return self._Ay
    @property
    def Az_seg(self) -> float:
        if self._Az_seg is None:
            zf = self.pntf.z
            rad = self.radius
            sango2 = self.sango2
            sinphi = self.sinphi
            self._Az_seg = 2/3*rad**3*sango2**3*sinphi+self._A_seg*zf
        return self._Az_seg
    @property
    def Az_line(self) -> float:
        if self._Az_line is None:
            ya = self.pnta.y
            za = self.pnta.z
            yb = self.pntb.y
            zb = self.pntb.z
            self._Az_line = (ya*zb-za*yb)*(za+zb)/6
        return self._Az_line
    @property
    def Az(self) -> float:
        if self._Az is None:
            self._Az = self.Az_seg+self.Az_line
        return self._Az
    @property
    def Ayy_seg(self) -> float:
        if self._Ayy_seg is None:
            yf = self.pntf.y
            rad = self.radius
            ang = self.ang
            sango2 = self.sango2
            sinang = self.sinang
            sinphi = self.sinphi
            cosphi = self.cosphi
            Ayy = rad**4/8*(ang-sinang+2*sinang*sango2**2)
            Azz = rad**4/8*(ang-sinang-2*sinang*sango2**2/3)
            self._Ayy_seg = Ayy*cosphi**2+Azz*sinphi**2+self.A_seg*yf**2
        return self._Ayy_seg
    @property
    def Ayy_line(self) -> float:
        if self._Ayy_line is None:
            ya = self.pnta.y
            za = self.pnta.z
            yb = self.pntb.y
            zb = self.pntb.z
            self._Ayy_line = (ya**2+ya*yb+yb**2)*(ya*zb-yb*za)/12
        return self._Ayy_line
    @property
    def Ayy(self) -> float:
        if self._Ayy is None:
            self._Ayy = self.Ayy_seg+self.Ayy_line
        return self._Ayy
    @property
    def Azz_seg(self) -> float:
        if self._Azz_seg is None:
            zf = self.pntf.z
            rad = self.radius
            ang = self.ang
            sango2 = self.sango2
            sinang = self.sinang
            sinphi = self.sinphi
            cosphi = self.cosphi
            Ayy = rad**4/8*(ang-sinang+2*sinang*sango2**2)
            Azz = rad**4/8*(ang-sinang-2*sinang*sango2**2/3)
            self._Azz_seg = Azz*cosphi**2+Ayy*sinphi**2+self.A_seg*zf**2
        return self._Azz_seg
    @property
    def Azz_line(self) -> float:
        if self._Azz_line is None:
            ya = self.pnta.y
            za = self.pnta.z
            yb = self.pntb.y
            zb = self.pntb.z
            self._Azz_line = (za**2+za*zb+zb**2)*(ya*zb-yb*za)/12
        return self._Azz_line
    @property
    def Azz(self) -> float:
        if self._Azz is None:
            self._Azz = self.Azz_seg+self.Azz_line
        return self._Azz
    @property
    def Ayz_seg(self) -> float:
        if self._Ayz_seg is None:
            yf = self.pntf.y
            zf = self.pntf.z
            rad = self.radius
            ang = self.ang
            sango2 = self.sango2
            sinang = self.sinang
            sinphi = self.sinphi
            cosphi = self.cosphi
            A_seg = rad**2/2*(ang-sinang)
            tempAyy = rad**4/8*(ang-sinang+2*sinang*sango2**2)
            tempAzz = rad**4/8*(ang-sinang-2*sinang*sango2**2/3)
            self._Ayz_seg = (tempAyy-tempAzz)*sinphi*cosphi+A_seg*yf*zf
        return self._Ayz_seg
    @property
    def Ayz_line(self) -> float:
        if self._Ayz_line is None:
            ya = self.pnta.y
            za = self.pnta.z
            yb = self.pntb.y
            zb = self.pntb.z
            self._Ayz_line = (ya*zb+2*ya*za+2*yb*zb+yb*za)*(ya*zb-yb*za)/24
        return self._Ayz_line
    @property
    def Ayz(self) -> float:
        if self._Ayz is None:
            self._Ayz = self.Ayz_seg + self.Ayz_line
        return self._Ayz
    def add_path(self, verts: Optional[List[Tuple[float, float]]]=None,
                 codes: Optional[List[float]]=None) -> Tuple[List[Tuple[float, float]],
                                                             List[float]]:
        if verts is None:
            verts = []
        if codes is None:
            codes = []
        if len(verts) == 0:
            verts.append((self.pnta.y, self.pnta.z))
            codes.append(1)
        verts.append((self.pntd.y, self.pntd.z))
        codes.append(4)
        verts.append((self.pnte.y, self.pnte.z))
        codes.append(4)
        verts.append((self.pntb.y, self.pntb.z))
        codes.append(4)
        return verts, codes
    def _repr_markdown_(self) -> str:
        table = MDTable()
        table.add_column('Point', 's')
        table.add_column('y', config.l1frm)
        table.add_column('z', config.l1frm)
        table.add_row(['pnta', self.pnta.y, self.pnta.z])
        table.add_row(['pntb', self.pntb.y, self.pntb.z])
        table.add_row(['pntc', self.pntc.y, self.pntc.z])
        table.add_row(['pntd', self.pntd.y, self.pntd.z])
        table.add_row(['pnte', self.pnte.y, self.pnte.z])
        table.add_row(['pntf', self.pntf.y, self.pntf.z])
        mdstr = table._repr_markdown_()
        table = MDTable()
        table.add_column('Type', 's')
        table.add_column('A', config.l2frm)
        table.add_column('Ay', config.l3frm)
        table.add_column('Az', config.l3frm)
        table.add_column('Ayy', config.l4frm)
        table.add_column('Azz', config.l4frm)
        table.add_column('Ayz', config.l4frm)
        table.add_row(['Segment', self.A_seg, self.Ay_seg, self.Az_seg,
                       self.Ayy_seg, self.Azz_seg, self.Ayz_seg])
        table.add_row(['Line', self.A_line, self.Ay_line, self.Az_line,
                       self.Ayy_line, self.Azz_line, self.Ayz_line])
        table.add_row(['Total', self.A, self.Ay, self.Az,
                       self.Ayy, self.Azz, self.Ayz])
        mdstr += table._repr_markdown_()
        return mdstr
    def __str__(self) -> str:
        table = MDTable()
        table.add_column('Point', 's')
        table.add_column('y', config.l1frm)
        table.add_column('z', config.l1frm)
        table.add_row(['pnta', self.pnta.y, self.pnta.z])
        table.add_row(['pntb', self.pntb.y, self.pntb.z])
        table.add_row(['pntc', self.pntc.y, self.pntc.z])
        table.add_row(['pntd', self.pntd.y, self.pntd.z])
        table.add_row(['pnte', self.pnte.y, self.pnte.z])
        table.add_row(['pntf', self.pntf.y, self.pntf.z])
        outstr = str(table)
        table = MDTable()
        table.add_column('Type', 's')
        table.add_column('A', config.l2frm)
        table.add_column('Ay', config.l3frm)
        table.add_column('Az', config.l3frm)
        table.add_column('Ayy', config.l4frm)
        table.add_column('Azz', config.l4frm)
        table.add_column('Ayz', config.l4frm)
        table.add_row(['Segment', self.A_seg, self.Ay_seg, self.Az_seg,
                       self.Ayy_seg, self.Azz_seg, self.Ayz_seg])
        table.add_row(['Line', self.A_line, self.Ay_line, self.Az_line,
                       self.Ayy_line, self.Azz_line, self.Ayz_line])
        table.add_row(['Total', self.A, self.Ay, self.Az,
                       self.Ayy, self.Azz, self.Ayz])
        outstr += str(table)
        return outstr
    def __repr__(self) -> str:
        return f'<Arc: {self.pnta}, {self.pntc}, {self.pntb}>'

def arc_from_points(pnta: Point, pntb: Point, pntc: Point, radius: float) -> Arc:
    dy1 = pnta.y - pntb.y
    dz1 = pnta.z - pntb.z
    dy2 = pntc.y - pntb.y
    dz2 = pntc.z - pntb.z
    l1 = sqrt(dy1**2 + dz1**2)
    l2 = sqrt(dy2**2 + dz2**2)
    dy1 = dy1/l1
    dz1 = dz1/l1
    dy2 = dy2/l2
    dz2 = dz2/l2
    sinab = dy2*dz1 - dz2*dy1
    cosab = dy1*dy2 + dz1*dz2
    cotabo2 = (1 + cosab)/sinab
    lp = abs(radius*cotabo2)
    yd = pntb.y + dy1*lp
    zd = pntb.z + dz1*lp
    ye = pntb.y + dy2*lp
    ze = pntb.z + dz2*lp
    pntf = determine_pntf(yd, zd, -dz1, dy1, ye, ze, -dz2, dy2)
    pntd = Point(yd, zd)
    pnte = Point(ye, ze)
    arc = Arc(pntd, pnte, pntb, pntf)
    return arc

def determine_pntf(ya, za, va, wa, yb, zb, vb, wb) -> Point:
    lbres = (va*za - va*zb - wa*ya + wa*yb)/(va*wb - vb*wa)
    yf = vb*lbres + yb
    zf = wb*lbres + zb
    return Point(yf, zf)
