from math import sqrt

from py2md.classes import MDTable

from .. import config
from .point import Point


class Line():
    pnta: Point = None
    pntb: Point = None
    _length: float = None
    _A: float = None
    _Ay: float = None
    _Az: float = None
    _Ayy: float = None
    _Azz: float = None
    _Ayz: float = None

    def __init__(self, pnta: Point, pntb: Point) -> None:
        self.pnta = pnta
        self.pntb = pntb

    @property
    def length(self) -> float:
        if self._length is None:
            dy = self.pntb.y-self.pnta.y
            dz = self.pntb.z-self.pnta.z
            self._length = sqrt(dy**2 + dz**2)
        return self._length

    @property
    def A(self) -> float:
        if self._A is None:
            ya = self.pnta.y
            za = self.pnta.z
            yb = self.pntb.y
            zb = self.pntb.z
            self._A = (ya*zb - za*yb)/2
        return self._A

    @property
    def Ay(self) -> float:
        if self._Ay is None:
            ya = self.pnta.y
            za = self.pnta.z
            yb = self.pntb.y
            zb = self.pntb.z
            self._Ay = (ya*zb - za*yb)*(ya + yb)/6
        return self._Ay

    @property
    def Az(self) -> float:
        if self._Az is None:
            ya = self.pnta.y
            za = self.pnta.z
            yb = self.pntb.y
            zb = self.pntb.z
            self._Az = (ya*zb - za*yb)*(za + zb)/6
        return self._Az

    @property
    def Ayy(self) -> float:
        if self._Ayy is None:
            ya = self.pnta.y
            za = self.pnta.z
            yb = self.pntb.y
            zb = self.pntb.z
            self._Ayy = (ya**2 + ya*yb + yb**2)*(ya*zb - yb*za)/12
        return self._Ayy

    @property
    def Azz(self) -> float:
        if self._Azz is None:
            ya = self.pnta.y
            za = self.pnta.z
            yb = self.pntb.y
            zb = self.pntb.z
            self._Azz = (za**2 + za*zb + zb**2)*(ya*zb - yb*za)/12
        return self._Azz

    @property
    def Ayz(self) -> float:
        if self._Ayz is None:
            ya = self.pnta.y
            za = self.pnta.z
            yb = self.pntb.y
            zb = self.pntb.z
            self._Ayz = (ya*zb + 2*ya*za + 2*yb*zb + yb*za)*(ya*zb - yb*za)/24
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
        verts.append((self.pntb.y, self.pntb.z))
        codes.append(2)
        return verts, codes

    def _repr_markdown_(self) -> str:
        table = MDTable()
        table.add_column('Point', 's')
        table.add_column('y', config.l1frm)
        table.add_column('z', config.l1frm)
        table.add_row(['pnta', self.pnta.y, self.pnta.z])
        table.add_row(['pntb', self.pntb.y, self.pntb.z])
        mdstr = table._repr_markdown_()
        table = MDTable()
        table.add_column('Type', 's')
        table.add_column('A', config.l2frm)
        table.add_column('Ay', config.l3frm)
        table.add_column('Az', config.l3frm)
        table.add_column('Ayy', config.l4frm)
        table.add_column('Azz', config.l4frm)
        table.add_column('Ayz', config.l4frm)
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
        outstr = table.__str__()
        table = MDTable()
        table.add_column('Type', 's')
        table.add_column('A', config.l2frm)
        table.add_column('Ay', config.l3frm)
        table.add_column('Az', config.l3frm)
        table.add_column('Ayy', config.l4frm)
        table.add_column('Azz', config.l4frm)
        table.add_column('Ayz', config.l4frm)
        table.add_row(['Total', self.A, self.Ay, self.Az,
                       self.Ayy, self.Azz, self.Ayz])
        outstr += table.__str__()
        return outstr

    def __repr__(self) -> str:
        return f'<Line: {self.pnta}, {self.pntb}>'
