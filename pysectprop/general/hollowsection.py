from math import atan, degrees, pi, sqrt

from matplotlib.patches import PathPatch
from matplotlib.path import Path
from matplotlib.pyplot import figure
from py2md.classes import MDHeading, MDTable

from .. import config
from .generalsection import GeneralSection


class Hole(GeneralSection):
    def check_area(self, display=True) -> None:
        self._A = None
        if self.A > 0.0:
            if display:
                print('Reversed coordinates.')
            self.y.reverse()
            self.z.reverse()
            self.r.reverse()
            self.generate_path()
        self._A = None

class HollowSection():
    outer: GeneralSection = None
    inner: Hole = None
    label: str = None
    _A: float = None
    _Ay: float = None
    _Az: float = None
    _cy: float = None
    _cz: float = None
    _Ayy: float = None
    _Azz: float = None
    _Ayz: float = None
    _Iyy: float = None
    _Izz: float = None
    _Iyz: float = None
    _Iav: float = None
    _Idf: float = None
    _Isq: float = None
    _thp: float = None
    _Iyp: float = None
    _Izp: float = None
    def __init__(self, outer: GeneralSection, inner: GeneralSection,
                 label: str=None) -> None:
        self.outer = outer
        inner.__class__ = Hole
        inner.reset()
        self.inner = inner
        self.label = label
        if label is not None:
            self.label = label
        self.generate_path()
        self.check_area()
    def check_area(self, display=True) -> None:
        self._A = None
        if self.A < 0.0:
            if display:
                print('Reversed coordinates.')
            self.outer.y.reverse()
            self.outer.z.reverse()
            self.outer.r.reverse()
            self.inner.y.reverse()
            self.inner.z.reverse()
            self.inner.r.reverse()
            self.generate_path()
        self._A = None
    def reset(self) -> None:
        for attr in self.__dict__:
            if attr[0] == '_':
                self.__dict__[attr] = None
        self.check_area(display=False)
    def generate_path(self) -> None:
        self.outer.generate_path()
        self.inner.generate_path()
    def mirror_y(self) -> None:
        self.reset()
        self.outer.mirror_y()
        self.inner.mirror_y()
    def mirror_z(self) -> None:
        self.reset()
        self.outer.mirror_z()
        self.inner.mirror_z()
    def translate(self, yt: float, zt: float) -> None:
        self.reset()
        self.outer.translate(yt, zt)
        self.inner.translate(yt, zt)
    def rotate(self, θr: float) -> None:
        self.reset()
        self.outer.rotate(θr)
        self.inner.rotate(θr)
    @property
    def A(self) -> float:
        if self._A is None:
            self._A = self.outer.A + self.inner.A
        return self._A
    @property
    def Ay(self) -> float:
        if self._Ay is None:
            self._Ay = self.outer.Ay + self.inner.Ay
        return self._Ay
    @property
    def Az(self) -> float:
        if self._Az is None:
            self._Az = self.outer.Az + self.inner.Az
        return self._Az
    @property
    def cy(self) -> float:
        if self._cy is None:
            self._cy = self.Ay/self.A
        return self._cy
    @property
    def cz(self) -> float:
        if self._cz is None:
            self._cz = self.Az/self.A
        return self._cz
    @property
    def Ayy(self) -> float:
        if self._Ayy is None:
            self._Ayy = self.outer.Ayy + self.inner.Ayy
        return self._Ayy
    @property
    def Azz(self) -> float:
        if self._Azz is None:
            self._Azz = self.outer.Azz + self.inner.Azz
        return self._Azz
    @property
    def Ayz(self) -> float:
        if self._Ayz is None:
            self._Ayz = self.outer.Ayz + self.inner.Ayz
        return self._Ayz
    @property
    def Iyy(self) -> float:
        if self._Iyy is None:
            self._Iyy = self.Azz - self.A*self.cz**2
        return self._Iyy
    @property
    def Izz(self) -> float:
        if self._Izz is None:
            self._Izz = self.Ayy - self.A*self.cy**2
        return self._Izz
    @property
    def Iyz(self) -> float:
        if self._Iyz is None:
            self._Iyz = self.Ayz - self.A*self.cy*self.cz
        return self._Iyz
    @property
    def Iav(self) -> float:
        if self._Iav is None:
            self._Iav = (self.Izz + self.Iyy)/2
        return self._Iav
    @property
    def Idf(self) -> float:
        if self._Idf is None:
            self._Idf = (self.Izz - self.Iyy)/2
        return self._Idf
    @property
    def Isq(self) -> float:
        if self._Isq is None:
            self._Isq = sqrt(self.Idf**2 + self.Iyz**2)
        return self._Isq
    @property
    def thp(self) -> float:
        if self._thp is None:
            tol = 1e-12
            if abs(self.Iyz)/self.Iav < tol:
                self._thp = 0.0
            elif abs(self.Idf)/self.Iav < tol:
                self._thp = pi/4
            else:
                self._thp = atan(self.Iyz/self.Idf)/2
        return self._thp
    @property
    def Iyp(self) -> float:
        if self._Iyp is None:
            self._Iyp = self.Iav + self.Isq
        return self._Iyp
    @property
    def Izp(self) -> float:
        if self._Izp is None:
            self._Izp = self.Iav - self.Isq
        return self._Izp
    def plot(self, ax=None):
        if ax is None:
            fig = figure(figsize=(12, 8))
            ax = fig.gca()
        verts = []
        codes = []
        for obj in self.outer.path:
            obj.add_path(verts, codes)
        p1 = Path(verts, codes)
        verts = []
        codes = []
        for obj in self.inner.path:
            obj.add_path(verts, codes)
        p2 = Path(verts, codes)
        p = PathPatch(Path.make_compound_path(p1, p2), alpha=0.8)
        ax.add_patch(p)
        ax.set_aspect('equal')
        ax.set_xlim(min(self.outer.y), max(self.outer.y))
        ax.set_ylim(min(self.outer.z), max(self.outer.z))
        return ax
    def plot_arc_control(self, ax=None):
        if ax is None:
            fig = figure(figsize=(12, 8))
            ax = fig.gca()
        self.outer.plot_arc_control(ax=ax)
        self.inner.plot_arc_control(ax=ax)
        return ax
    def section_heading(self, head: str):
        if self.label is None:
            head = f'{head:s}'
        else:
            head = f'{head:s} - {self.label:s}'
        heading = MDHeading(head, 3)
        return str(heading)
    def section_properties(self, nohead: bool=True, outtype: str='md'):
        lunit = config.lunit
        l1frm = config.l1frm
        l2frm = config.l2frm
        l3frm = config.l3frm
        l4frm = config.l4frm
        angfrm = config.angfrm
        mdstr = ''
        if not nohead:
            mdstr += self.section_heading('Hollow Section')
        table = MDTable()
        if outtype == 'md':
            table.add_column(f'A ({lunit:s}<sup>2</sup>)', l2frm, data=[self.A])
            table.add_column(f'Ay ({lunit:s}<sup>3</sup>)', l3frm, data=[self.Ay])
            table.add_column(f'Az ({lunit:s}<sup>3</sup>)', l3frm, data=[self.Az])
            table.add_column(f'c<sub>y</sub> ({lunit:s})', l1frm, data=[self.cy])
            table.add_column(f'c<sub>z</sub> ({lunit:s})', l1frm, data=[self.cz])
            table.add_column(f'Ayy ({lunit:s}<sup>4</sup>)', l4frm, data=[self.Ayy])
            table.add_column(f'Azz ({lunit:s}<sup>4</sup>)', l4frm, data=[self.Azz])
            table.add_column(f'Ayz ({lunit:s}<sup>4</sup>)', l4frm, data=[self.Ayz])
            mdstr += table._repr_markdown_()
        else:
            table.add_column(f'A ({lunit:s}^2)', l2frm, data=[self.A])
            table.add_column(f'Ay ({lunit:s}^3)', l3frm, data=[self.Ay])
            table.add_column(f'Az ({lunit:s}^3)', l3frm, data=[self.Az])
            table.add_column(f'c_y ({lunit:s})', l1frm, data=[self.cy])
            table.add_column(f'c_z ({lunit:s})', l1frm, data=[self.cz])
            table.add_column(f'Ayy ({lunit:s}^4)', l4frm, data=[self.Ayy])
            table.add_column(f'Azz ({lunit:s}^4)', l4frm, data=[self.Azz])
            table.add_column(f'Ayz ({lunit:s}^4)', l4frm, data=[self.Ayz])
            mdstr += str(table)
        table = MDTable()
        if outtype == 'md':
            table.add_column(f'I<sub>yy</sub> ({lunit:s}<sup>4</sup>)',
                            l4frm, data=[self.Iyy])
            table.add_column(f'I<sub>zz</sub> ({lunit:s}<sup>4</sup>)',
                            l4frm, data=[self.Izz])
            table.add_column(f'I<sub>yz</sub> ({lunit:s}<sup>4</sup>)',
                            l4frm, data=[self.Iyz])
            table.add_column('&theta;<sub>p</sub> (&deg;)',
                            angfrm, data=[degrees(self.thp)])
            table.add_column(f'I<sub>yp</sub> ({lunit:s}<sup>4</sup>)',
                            l4frm, data=[self.Iyp])
            table.add_column(f'I<sub>zp</sub> ({lunit:s}<sup>4</sup>)',
                            l4frm, data=[self.Izp])
            mdstr += table._repr_markdown_()
        else:
            table.add_column(f'I_yy ({lunit:s}^4)',
                            l4frm, data=[self.Iyy])
            table.add_column(f'I_zz ({lunit:s}^4)',
                            l4frm, data=[self.Izz])
            table.add_column(f'I_yz ({lunit:s}^4)',
                            l4frm, data=[self.Iyz])
            table.add_column('th_p (deg)',
                            angfrm, data=[degrees(self.thp)])
            table.add_column(f'I_yp ({lunit:s}^4)',
                            l4frm, data=[self.Iyp])
            table.add_column(f'I_zp ({lunit:s}^4)',
                            l4frm, data=[self.Izp])
            mdstr += str(table)
        return mdstr
    def _repr_markdown_(self) -> str:
        return self.section_properties(nohead=False, outtype='md')
    def __str__(self) -> str:
        return self.section_properties(nohead=False, outtype='str')
    def __repr__(self) -> str:
        if self.label is None:
            outstr = '<HollowSection>'
        else:
            outstr = f'<HollowSection {self.label:s}>'
        return outstr
