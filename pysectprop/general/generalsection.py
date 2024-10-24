from math import cos, radians, sin
from typing import TYPE_CHECKING

from matplotlib.patches import PathPatch
from matplotlib.path import Path
from matplotlib.pyplot import figure
from py2md.classes import MDTable

from .. import config
from .arc import Arc, arc_from_points
from .line import Line
from .numericalsection import NumericalSection
from .point import Point

if TYPE_CHECKING:
    from matplotlib.axes import Axes


class GeneralSection(NumericalSection):
    y: list[float] = None
    z: list[float] = None
    r: list[float] = None
    pnts: list[Point] = None
    path: list[Line | Arc] = None

    def __init__(self, y: list[float], z: list[float], r: list[float],
                 label: str = None) -> None:
        newy, newz, newr = cleanup_points(y, z, r)
        self.y = newy
        self.z = newz
        self.r = newr
        super().__init__(label)
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
        lines: list[Line] = []
        for i in range(numpnt):
            a = i
            b = i+1
            if b == numpnt:
                b = 0
            pnta = pnts[a]
            pntb = pnts[b]
            line = Line(pnta, pntb)
            lines.append(line)
        arcs: list[Arc] = []
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
        y = [yi + yt for yi in self.y]
        self.y = y
        z = [zi + zt for zi in self.z]
        self.z = z
        self.reset()
        self.generate_path()
        self.check_area(display=False)

    def rotate(self, theta: float) -> None:
        thrad = radians(theta)
        costh = cos(thrad)
        sinth = sin(thrad)
        y = [yi*costh - zi*sinth for yi, zi in zip(self.y, self.z)]
        z = [zi*costh + yi*sinth for yi, zi in zip(self.y, self.z)]
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

    def plot(self, ax: 'Axes | None' = None) -> 'Axes':
        if ax is None:
            fig = figure(figsize=(12, 8))
            ax = fig.gca()
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

    def plot_arc_control(self, ax: 'Axes | None' = None) -> 'Axes':
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

    @property
    def build_up_table(self) -> MDTable:
        table = MDTable()
        table.add_column('Item', 's')
        table.add_column('Type', 's')
        table.add_column('A', config.l2frm)
        table.add_column('Ay', config.l3frm)
        table.add_column('Az', config.l3frm)
        table.add_column('Ayy', config.l4frm)
        table.add_column('Azz', config.l4frm)
        table.add_column('Ayz', config.l4frm)
        for i, obj in enumerate(self.path):
            table.add_row([str(i+1), type(obj).__name__, obj.A, obj.Ay, obj.Az,
                           obj.Ayy, obj.Azz, obj.Ayz])
        table.add_row(['Total', '', self.A, self.Ay, self.Az,
                       self.Ayy, self.Azz, self.Ayz])
        return table

    def _repr_markdown_(self) -> str:
        mdstr = self.section_heading('General Section')
        mdstr += self.section_properties(outtype='md')
        return mdstr

    def __str__(self) -> str:
        mdstr = self.section_heading('General Section')
        mdstr += self.section_properties(outtype=str)
        return mdstr

    def __repr__(self) -> str:
        if self.label is None:
            outstr = '<GeneralSection>'
        else:
            outstr = f'<GeneralSection {self.label:s}>'
        return outstr

def cleanup_points(y: list[float], z: list[float],
                   r: list[float]) -> tuple[list[float], list[float], list[float]]:
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
