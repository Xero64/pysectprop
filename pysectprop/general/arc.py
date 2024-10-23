from math import sqrt

from py2md.classes import MDTable

from .. import config
from .line import Line
from .point import Point
from .sector import Sector


class Arc():
    pnta: Point = None
    pntb: Point = None
    pntc: Point = None
    pntf: Point = None
    _K: float = None
    _pntd: Point = None
    _pnte: Point = None
    _lineaf: Line = None
    _linefb: Line = None
    _sector: Sector = None
    _A: float = None
    _Ay: float = None
    _Az: float = None
    _Ayy: float = None
    _Azz: float = None
    _Ayz: float = None

    def __init__(self, pnta: Point, pntb: Point, pntc: Point, pntf: Point) -> None:
        self.pnta = pnta
        self.pntb = pntb
        self.pntc = pntc
        self.pntf = pntf

    @property
    def K(self) -> float:
        if self._K is None:
            self._K = calculate_K(self.pnta, self.pntb, self.pntc)
        return self._K

    @property
    def pntd(self) -> Point:
        if self._pntd is None:
            dy1 = self.pnta.y - self.pntc.y
            dz1 = self.pnta.z - self.pntc.z
            yd = self.pntc.y + dy1*self.K
            zd = self.pntc.z + dz1*self.K
            self._pntd = Point(yd, zd)
        return self._pntd

    @property
    def pnte(self) -> Point:
        if self._pnte is None:
            dy2 = self.pntb.y - self.pntc.y
            dz2 = self.pntb.z - self.pntc.z
            ye = self.pntc.y + dy2*self.K
            ze = self.pntc.z + dz2*self.K
            self._pnte = Point(ye, ze)
        return self._pnte

    @property
    def lineaf(self) -> Line:
        if self._lineaf is None:
            self._lineaf = Line(self.pnta, self.pntf)
        return self._lineaf

    @property
    def linefb(self) -> Line:
        if self._linefb is None:
            self._linefb = Line(self.pntf, self.pntb)
        return self._linefb

    @property
    def sector(self) -> Sector:
        if self._sector is None:
            self._sector = Sector(self.pnta, self.pntb, self.pntf)
        return self._sector

    @property
    def A(self) -> float:
        if self._A is None:
            self._A = self.sector.A + self.lineaf.A + self.linefb.A
        return self._A

    @property
    def Ay(self) -> float:
        if self._Ay is None:
            self._Ay = self.sector.Ay + self.lineaf.Ay + self.linefb.Ay
        return self._Ay

    @property
    def Az(self) -> float:
        if self._Az is None:
            self._Az = self.sector.Az + self.lineaf.Az + self.linefb.Az
        return self._Az

    @property
    def Ayy(self) -> float:
        if self._Ayy is None:
            self._Ayy = self.sector.Ayy + self.lineaf.Ayy + self.linefb.Ayy
        return self._Ayy

    @property
    def Azz(self) -> float:
        if self._Azz is None:
            self._Azz = self.sector.Azz + self.lineaf.Azz + self.linefb.Azz
        return self._Azz

    @property
    def Ayz(self) -> float:
        if self._Ayz is None:
            self._Ayz = self.sector.Ayz + self.lineaf.Ayz + self.linefb.Ayz
        return self._Ayz

    def add_path(self, verts: list[tuple[float, float]] | None = None,
                 codes: list[float] | None = None) -> tuple[list[tuple[float, float]],
                                                            list[float]]:
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
        table.add_row(['Sector', self.sector.A, self.sector.Ay, self.sector.Az,
                       self.sector.Ayy, self.sector.Azz, self.sector.Ayz])
        table.add_row(['Line A-F', self.lineaf.A, self.lineaf.Ay, self.lineaf.Az,
                       self.lineaf.Ayy, self.lineaf.Azz, self.lineaf.Ayz])
        table.add_row(['Line F-B', self.linefb.A, self.linefb.Ay, self.linefb.Az,
                       self.linefb.Ayy, self.linefb.Azz, self.linefb.Ayz])
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
        outstr = table.__str__()
        table = MDTable()
        table.add_column('Type', 's')
        table.add_column('A', config.l2frm)
        table.add_column('Ay', config.l3frm)
        table.add_column('Az', config.l3frm)
        table.add_column('Ayy', config.l4frm)
        table.add_column('Azz', config.l4frm)
        table.add_column('Ayz', config.l4frm)
        table.add_row(['Sector', self.sector.A, self.sector.Ay, self.sector.Az,
                       self.sector.Ayy, self.sector.Azz, self.sector.Ayz])
        table.add_row(['Line A-F', self.lineaf.A, self.lineaf.Ay, self.lineaf.Az,
                       self.lineaf.Ayy, self.lineaf.Azz, self.lineaf.Ayz])
        table.add_row(['Line F-B', self.linefb.A, self.linefb.Ay, self.linefb.Az,
                       self.linefb.Ayy, self.linefb.Azz, self.linefb.Ayz])
        table.add_row(['Total', self.A, self.Ay, self.Az,
                       self.Ayy, self.Azz, self.Ayz])
        outstr += table.__str__()
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

def calculate_K(pnta: Point, pntb: Point, pntc: Point) -> float:
    dya = pntc.y - pnta.y
    dza = pntc.z - pnta.z
    dyb = pntb.y - pntc.y
    dzb = pntb.z - pntc.z
    adb = dya*dyb + dza*dzb
    abm = sqrt(dya**2 + dza**2)*sqrt(dyb**2 + dzb**2)
    Kv = 1 - 4*sqrt(adb + abm)/(3*(sqrt(2)*sqrt(abm) + sqrt(adb + abm)))
    return Kv

def determine_pntf(ya: float, za: float, va: float, wa: float,
                   yb: float, zb: float, vb: float, wb: float) -> Point:
    lbres = (va*za - va*zb - wa*ya + wa*yb)/(va*wb - vb*wa)
    yf = vb*lbres + yb
    zf = wb*lbres + zb
    return Point(yf, zf)
