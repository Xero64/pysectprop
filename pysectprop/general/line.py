from py2md.classes import MDTable
from .point import Point
from .. import config

class Line(object):
    pnta = None
    pntb = None
    length = None
    diry = None
    dirz = None
    _A = None
    _Ay = None
    _Az = None
    _Ayy = None
    _Azz = None
    _Ayz = None
    def __init__(self, pnta: Point, pntb: Point):
        self.pnta = pnta
        self.pntb = pntb
        self.update()
    def update(self):
        dy = self.pntb.y-self.pnta.y
        dz = self.pntb.z-self.pnta.z
        self.length = (dy**2+dz**2)**0.5
        if self.length == 0.0:
            self.diry = 0.0
            self.dirz = 0.0
        else:
            self.diry = dy/self.length
            self.dirz = dz/self.length
    def add_path(self, verts: list=None, codes: list=None):
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
    @property
    def A(self):
        if self._A is None:
            ya = self.pnta.y
            za = self.pnta.z
            yb = self.pntb.y
            zb = self.pntb.z
            self._A = (ya*zb-za*yb)/2
        return self._A
    @property
    def Ay(self):
        if self._Ay is None:
            ya = self.pnta.y
            za = self.pnta.z
            yb = self.pntb.y
            zb = self.pntb.z
            self._Ay = (ya*zb-za*yb)*(ya+yb)/6
        return self._Ay
    @property
    def Az(self):
        if self._Az is None:
            ya = self.pnta.y
            za = self.pnta.z
            yb = self.pntb.y
            zb = self.pntb.z
            self._Az = (ya*zb-za*yb)*(za+zb)/6
        return self._Az
    @property
    def Ayy(self):
        if self._Ayy is None:
            ya = self.pnta.y
            za = self.pnta.z
            yb = self.pntb.y
            zb = self.pntb.z
            self._Ayy = (ya**2+ya*yb+yb**2)*(ya*zb-yb*za)/12
        return self._Ayy
    @property
    def Azz(self):
        if self._Azz is None:
            ya = self.pnta.y
            za = self.pnta.z
            yb = self.pntb.y
            zb = self.pntb.z
            self._Azz = (za**2+za*zb+zb**2)*(ya*zb-yb*za)/12
        return self._Azz
    @property
    def Ayz(self):
        if self._Ayz is None:
            ya = self.pnta.y
            za = self.pnta.z
            yb = self.pntb.y
            zb = self.pntb.z
            self._Ayz = (ya*zb+2*ya*za+2*yb*zb+yb*za)*(ya*zb-yb*za)/24
        return self._Ayz
    def __repr__(self):
        return '<Line: {:}, {:}>'.format(self.pnta.__repr__(),
                                         self.pntb.__repr__())
    def __str__(self):
        table = MDTable()
        table.add_column('Point', 's')
        table.add_column('y', config.l1frm)
        table.add_column('z', config.l1frm)
        table.add_row(['pnta', self.pnta.y, self.pnta.z])
        table.add_row(['pntb', self.pntb.y, self.pntb.z])
        mdstr = str(table)
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
        mdstr += str(table)
        return mdstr
    def _repr_markdown_(self):
        return self.__str__()
