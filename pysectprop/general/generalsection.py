from typing import List, Union, Tuple

from math import atan, cos, sin, degrees, pi, radians
from matplotlib.pyplot import figure
from py2md.classes import MDHeading, MDTable
from .point import Point
from .line import Line
from .arc import Arc, arc_from_points
from .. import config

class GeneralSection():
    y: List[float] = None
    z: List[float] = None
    r: List[float] = None
    label: str = None
    pnts: List[Point] = None
    path: List[Union[Line, Arc]] = None
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
    _thp: float = None
    _Iyp: float = None
    _Izp: float = None
    def __init__(self, y: List[float], z: List[float], r: List[float],
                 label: str=None) -> None:
        newy, newz, newr = cleanup_points(y, z, r)
        self.y = newy
        self.z = newz
        self.r = newr
        if label is not None:
            self.label = label
        self.generate_path()
        self.check_area()
    def check_area(self, display=True) -> None:
        self._A = None
        if self.A < 0.0:
            if display:
                print('Reversed coordinates.')
            self.y.reverse()
            self.z.reverse()
            self.r.reverse()
            self.generate_path()
        self._A = None
    def generate_path(self) -> None:
        numpnt = len(self.r)
        pnts = []
        for i in range(numpnt):
            yi = self.y[i]
            zi = self.z[i]
            pnts.append(Point(yi, zi))
        lines: List[Line] = []
        for i in range(numpnt):
            a = i
            b = i+1
            if b == numpnt:
                b = 0
            pnta = pnts[a]
            pntb = pnts[b]
            line = Line(pnta, pntb)
            lines.append(line)
        arcs: List[Arc] = []
        for i in range(numpnt):
            radius = self.r[i]
            if i == 0:
                a = -1
            else:
                a = i-1
            b = i
            linea = lines[a]
            lineb = lines[b]
            pnta = linea.pnta
            pntb = linea.pntb
            pntc = lineb.pntb
            if radius != 0.0:
                arc = arc_from_points(pnta, pntb, pntc, radius)
            else:
                arc = None
            arcs.append(arc)
        lentol = 1e-12
        self.path = []
        for i in range(numpnt):
            a = i
            b = i+1
            if b == numpnt:
                b = 0
            arca = arcs[a]
            arcb = arcs[b]
            linea = lines[a]
            if arca is None:
                pnta = linea.pnta
            else:
                self.path.append(arca)
                pnta = arca.pntb
            if arcb is None:
                pntb = linea.pntb
            else:
                pntb = arcb.pnta
            line = Line(pnta, pntb)
            if line.length > lentol:
                self.path.append(line)
        self.pnts = []
        for obj in self.path:
            self.pnts.append(obj.pnta)
    def reset(self) -> None:
        self._A = None
        self._Ay = None
        self._Az = None
        self._cy = None
        self._cz = None
        self._Ayy = None
        self._Azz = None
        self._Ayz = None
        self._Iyy = None
        self._Izz = None
        self._Iyz = None
        self._thp = None
        self._Iyp = None
        self._Izp = None
        self.check_area(display=False)
    def mirror_y(self) -> None:
        z = [-zi for zi in self.z]
        self.z = z
        self.reset()
        self.generate_path()
        self.check_area(display=False)
    def mirror_z(self) -> None:
        y = [-yi for yi in self.y]
        self.y = y
        self.reset()
        self.generate_path()
        self.check_area(display=False)
    def translate(self, yt: float, zt: float) -> None:
        y = [-yi+yt for yi in self.y]
        self.y = y
        z = [-zi+zt for zi in self.z]
        self.z = z
        self.reset()
        self.generate_path()
        self.check_area(display=False)
    def rotate(self, θr: float) -> None:
        thrad = radians(θr)
        costh = cos(thrad)
        sinth = sin(thrad)
        y = [yi*costh-zi*sinth for yi, zi in zip(self.y, self.z)]
        z = [zi*costh+yi*sinth for yi, zi in zip(self.y, self.z)]
        self.y = y
        self.z = z
        self.reset()
        self.generate_path()
        self.check_area(display=False)
    @property
    def A(self) -> float:
        if self._A is None:
            self._A = 0.0
            for obj in self.path:
                self._A += obj.A
        return self._A
    @property
    def Ay(self) -> float:
        if self._Ay is None:
            self._Ay = 0.0
            for obj in self.path:
                self._Ay += obj.Ay
        return self._Ay
    @property
    def Az(self) -> float:
        if self._Az is None:
            self._Az = 0.0
            for obj in self.path:
                self._Az += obj.Az
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
            self._Ayy = 0.0
            for obj in self.path:
                self._Ayy += obj.Ayy
        return self._Ayy
    @property
    def Azz(self) -> float:
        if self._Azz is None:
            self._Azz = 0.0
            for obj in self.path:
                self._Azz += obj.Azz
        return self._Azz
    @property
    def Ayz(self) -> float:
        if self._Ayz is None:
            self._Ayz = 0.0
            for obj in self.path:
                self._Ayz += obj.Ayz
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
    def thp(self) -> float:
        if self._thp is None:
            tol = 1e-12
            if abs(2*self.Iyz) < tol:
                self._thp = 0.0
            elif abs(self.Izz-self.Iyy) < tol:
                self._thp = pi/4
            else:
                self._thp = atan(2*self.Iyz/(self.Izz-self.Iyy))/2
        return self._thp
    @property
    def Iyp(self) -> float:
        if self._Iyp is None:
            c = cos(self.thp)
            s = sin(self.thp)
            self._Iyp = self.Iyy*c**2+self.Izz*s**2-2*self.Iyz*c*s
        return self._Iyp
    @property
    def Izp(self) -> float:
        if self._Izp is None:
            c = cos(self.thp)
            s = sin(self.thp)
            self._Izp = self.Iyy*s**2+self.Izz*c**2+2*self.Iyz*c*s
        return self._Izp
    def plot(self, ax=None):
        if ax is None:
            fig = figure(figsize=(12, 8))
            ax = fig.gca()
        from matplotlib.path import Path
        from matplotlib.patches import PathPatch
        verts = []
        codes = []
        for obj in self.path:
            obj.add_path(verts, codes)
        path = Path(verts, codes)
        patch = PathPatch(path, alpha=0.8)
        ax.set_aspect('equal')
        ax.add_patch(patch)
        ax.set_xlim(min(self.y), max(self.y))
        ax.set_ylim(min(self.z), max(self.z))
        return ax
    def plot_arc_control(self, ax=None):
        if ax is None:
            fig = figure(figsize=(12, 8))
            ax = fig.gca()
        for obj in self.path:
            if isinstance(obj, Arc):
                y = [obj.pntf.y, obj.pnta.y, obj.pntd.y,
                     obj.pnte.y, obj.pntb.y, obj.pntf.y]
                z = [obj.pntf.z, obj.pnta.z, obj.pntd.z,
                     obj.pnte.z, obj.pntb.z, obj.pntf.z]
                ax.plot(y, z)
        return ax
    def build_up_table(self):
        table = MDTable()
        table.add_column('Item', '')
        table.add_column('A', config.l2frm)
        table.add_column('Ay', config.l3frm)
        table.add_column('Az', config.l3frm)
        table.add_column('Ayy', config.l4frm)
        table.add_column('Azz', config.l4frm)
        table.add_column('Ayz', config.l4frm)
        for i, obj in enumerate(self.path):
            table.add_row([i+1, obj.A, obj.Ay, obj.Az, obj.Ayy, obj.Azz, obj.Ayz])
        table.add_row(['Total', self.A, self.Ay, self.Az, self.Ayy, self.Azz, self.Ayz])
        return table
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
            mdstr += self.section_heading('General Section')
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
            outstr = '<GeneralSection>'
        else:
            outstr = f'<GeneralSection {self.label:s}>'
        return outstr

def cleanup_points(y: List[float], z: List[float],
                   r: List[float]) -> Tuple[List[float], List[float], List[float]]:
    keep = []
    num = len(y)
    for i in range(num):
        a, b = i-1, i
        if a < 0:
            a = num-1
        ya, za = y[a], z[a]
        yb, zb = y[b], z[b]
        if ya == yb and za == zb:
            keep.append(False)
        else:
            keep.append(True)
    newy, newz, newr = [], [], []
    for i in range(num):
        if keep[i]:
            newy.append(y[i])
            newz.append(z[i])
            newr.append(r[i])
        else:
            print('Duplicate point removed.')
    return newy, newz, newr
