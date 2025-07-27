from math import atan2, cos, degrees, radians, sin
from typing import TYPE_CHECKING

from matplotlib.patches import Rectangle
from matplotlib.pyplot import figure
from py2md.classes import MDHeading, MDTable

from .. import config
from .numericalsection import NumericalSection

if TYPE_CHECKING:
    from matplotlib.axes import Axes


class ThinWalledSection(NumericalSection):
    y: list[float] = None
    z: list[float] = None
    t: list[float] = None
    label: str = None
    segs: list['WallSegment'] = None

    def __init__(self, y: list, z: list, t: list, label: str=None) -> None:
        lent = len(t)
        leny = len(y)
        lenz = len(z)
        if leny != lenz:
            print('The length of y does not equal the length of z.')
            return
        if lent != leny and lent != leny-1:
            print('The length of thickness is not consistant with the geometry.')
            return
        self.y = y
        self.z = z
        self.t = t
        self.label = label
        self.generate_segments()

    def check_area(self, display=True) -> None:
        self._A = None
        if self.A < 0.0:
            if display:
                print('Reversed coordinates.')
            self.y.reverse()
            self.z.reverse()
            self.t.reverse()
            self.generate_segments()
        self._A = None

    def reset(self) -> None:
        for attr in self.__dict__:
            if attr[0] == '_':
                self.__dict__[attr] = None
        self.check_area(display=False)

    def generate_segments(self) -> None:
        lent = len(self.t)
        lenp = len(self.y)
        self.segs = []
        for i in range(lent-1):
            ya = self.y[i]
            za = self.z[i]
            yb = self.y[i+1]
            zb = self.z[i+1]
            ts = self.t[i]
            ws = WallSegment(ya, za, yb, zb, ts)
            self.segs.append(ws)
        if lenp > lent:
            ya = self.y[-2]
            za = self.z[-2]
            yb = self.y[-1]
            zb = self.z[-1]
            ts = self.t[-1]
        else:
            ya = self.y[-1]
            za = self.z[-1]
            yb = self.y[0]
            zb = self.z[0]
            ts = self.t[-1]
        ws = WallSegment(ya, za, yb, zb, ts)
        self.segs.append(ws)
        if lenp != lent:
            self.segs[0].set_free_at_a(True)
            self.segs[-1].set_free_at_b(True)

    def mirror_y(self) -> None:
        z = [-zi for zi in self.z]
        self.z = z
        self.reset()
        self.generate_segments()
        self.check_area(display=False)

    def mirror_z(self) -> None:
        y = [-yi for yi in self.y]
        self.y = y
        self.reset()
        self.generate_segments()
        self.check_area(display=False)

    def translate(self, yt: float, zt: float) -> None:
        y = [yi + yt for yi in self.y]
        self.y = y
        z = [zi + zt for zi in self.z]
        self.z = z
        self.reset()
        self.generate_segments()
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
        self.generate_segments()
        self.check_area(display=False)

    @property
    def A(self) -> float:
        if self._A is None:
            self._A = 0.0
            for seg in self.segs:
                self._A += seg.A
        return self._A

    @property
    def Ay(self) -> float:
        if self._Ay is None:
            self._Ay = 0.0
            for seg in self.segs:
                self._Ay += seg.Ay
        return self._Ay

    @property
    def Az(self) -> float:
        if self._Az is None:
            self._Az = 0.0
            for seg in self.segs:
                self._Az += seg.Az
        return self._Az

    @property
    def Ayy(self) -> float:
        if self._Ayy is None:
            self._Ayy = 0.0
            for seg in self.segs:
                self._Ayy += seg.Ayy
        return self._Ayy

    @property
    def Azz(self) -> float:
        if self._Azz is None:
            self._Azz = 0.0
            for seg in self.segs:
                self._Azz += seg.Azz
        return self._Azz

    @property
    def Ayz(self) -> float:
        if self._Ayz is None:
            self._Ayz = 0.0
            for seg in self.segs:
                self._Ayz += seg.Ayz
        return self._Ayz

    def plot(self, ax: 'Axes'=None) -> 'Axes':
        if ax is None:
            fig = figure(figsize=(12, 8))
            ax = fig.gca()
        from matplotlib.collections import PatchCollection
        rects = []
        for seg in self.segs:
            rects.append(seg.mpl_rectangle())
        patchcol = PatchCollection(rects)
        ax.add_collection(patchcol)
        ax.set_aspect('equal')
        miny = min(self.y)
        maxy = max(self.y)
        minz = min(self.z)
        maxz = max(self.z)
        maxt = max(self.t)
        ax.set_xlim(miny-maxt/2, maxy+maxt/2)
        ax.set_ylim(minz-maxt/2, maxz+maxt/2)
        return ax

    def _repr_markdown_(self) -> str:
        lunit = config.lunit
        l1frm = config.l1frm
        l2frm = config.l2frm
        l3frm = config.l3frm
        l4frm = config.l4frm
        angfrm = config.angfrm
        if self.label is None:
            head = 'Thin-Walled Section Properties'
        else:
            head = f'Thin-Walled Section Properties - {self.label:s}'
        heading = MDHeading(head, 3)
        mdstr = str(heading)
        table = MDTable()
        table.add_column(f'A ({lunit:s}<sup>2</sup>)', l2frm, data=[self.A])
        table.add_column(f'Ay ({lunit:s}<sup>3</sup>)', l3frm, data=[self.Ay])
        table.add_column(f'Az ({lunit:s}<sup>3</sup>)', l3frm, data=[self.Az])
        table.add_column(f'c<sub>y</sub> ({lunit:s})', l1frm, data=[self.cy])
        table.add_column(f'c<sub>z</sub> ({lunit:s})', l1frm, data=[self.cz])
        table.add_column(f'Ayy ({lunit:s}<sup>4</sup>)', l4frm, data=[self.Ayy])
        table.add_column(f'Azz ({lunit:s}<sup>4</sup>)', l4frm, data=[self.Azz])
        table.add_column(f'Ayz ({lunit:s}<sup>4</sup>)', l4frm, data=[self.Ayz])
        mdstr += table._repr_markdown_()
        table = MDTable()
        table.add_column(f'I<sub>yy</sub> ({lunit:s}<sup>4</sup>)', l4frm,
                         data=[self.Iyy])
        table.add_column(f'I<sub>zz</sub> ({lunit:s}<sup>4</sup>)', l4frm,
                         data=[self.Izz])
        table.add_column(f'I<sub>yz</sub> ({lunit:s}<sup>4</sup>)', l4frm,
                         data=[self.Iyz])
        table.add_column('&theta;<sub>p</sub> (&deg;)', angfrm,
                         data=[degrees(self.thp)])
        table.add_column(f'I<sub>yp</sub> ({lunit:s}<sup>4</sup>)', l4frm,
                         data=[self.Iyp])
        table.add_column(f'I<sub>zp</sub> ({lunit:s}<sup>4</sup>)', l4frm,
                         data=[self.Izp])
        mdstr += table._repr_markdown_()
        return mdstr

    def __str__(self) -> str:
        lunit = config.lunit
        l1frm = config.l1frm
        l2frm = config.l2frm
        l3frm = config.l3frm
        l4frm = config.l4frm
        angfrm = config.angfrm
        if self.label is None:
            head = 'Thin-Walled Section Properties'
        else:
            head = f'Thin-Walled Section Properties - {self.label:s}'
        heading = MDHeading(head, 3)
        outstr = str(heading)
        table = MDTable()
        table.add_column(f'A ({lunit:s}^2)', l2frm, data=[self.A])
        table.add_column(f'Ay ({lunit:s}^3)', l3frm, data=[self.Ay])
        table.add_column(f'Az ({lunit:s}^3)', l3frm, data=[self.Az])
        table.add_column(f'c_y ({lunit:s})', l1frm, data=[self.cy])
        table.add_column(f'c_z ({lunit:s})', l1frm, data=[self.cz])
        table.add_column(f'Ayy ({lunit:s}^4)', l4frm, data=[self.Ayy])
        table.add_column(f'Azz ({lunit:s}^4)', l4frm, data=[self.Azz])
        table.add_column(f'Ayz ({lunit:s}^4)', l4frm, data=[self.Ayz])
        outstr += table.__str__()
        table = MDTable()
        table.add_column(f'I_yy ({lunit:s}^4)', l4frm,
                         data=[self.Iyy])
        table.add_column(f'I_zz ({lunit:s}^4)', l4frm,
                         data=[self.Izz])
        table.add_column(f'I_yz ({lunit:s}^4)', l4frm,
                         data=[self.Iyz])
        table.add_column('th_p (deg)', angfrm,
                         data=[degrees(self.thp)])
        table.add_column(f'I_yp ({lunit:s}^4)', l4frm,
                         data=[self.Iyp])
        table.add_column(f'I_zp ({lunit:s}^4)', l4frm,
                         data=[self.Izp])
        outstr += table.__str__()
        return outstr

    def __repr__(self) -> str:
        if self.label is None:
            outstr = '<ThinWalledSection>'
        else:
            outstr = f'<ThinWalledSection {self.label:s}>'
        return outstr

class WallSegment():
    ya: float = None
    za: float = None
    yb: float = None
    zb: float = None
    ts: float = None
    fa: float = None
    fb: float = None
    dy: float = None
    dz: float = None
    ls: float = None
    th: float = None
    _A: float = None
    _Ay: float = None
    _Az: float = None
    _cy: float = None
    _cz: float= None
    _Ayy: float = None
    _Azz: float = None
    _Ayz: float = None
    _Iyy: float = None
    _Izz: float = None
    _Iyz: float = None
    _thp: float = None
    _Iyp: float = None
    _Izp: float = None

    def __init__(self, ya: float, za: float, yb: float, zb: float, ts: float) -> None:
        self.ya = ya
        self.za = za
        self.yb = yb
        self.zb = zb
        self.ts = ts
        self.update()

    def update(self) -> None:
        self.fa = False
        self.fb = False
        self.dy = self.yb-self.ya
        self.dz = self.zb-self.za
        self.ls = (self.dy**2+self.dz**2)**0.5
        self.th = degrees(atan2(self.dz, self.dy))

    def set_free_at_a(self, fa) -> None:
        self.fa = fa

    def set_free_at_b(self, fb) -> None:
        self.fb = fb

    def is_oef(self) -> bool:
        if self.fa and not self.fb:
            return True
        if not self.fa and self.fb:
            return True
        return False

    def is_nef(self) -> bool:
        if not self.fa and not self.fb:
            return True
        return False

    @property
    def A(self) -> float:
        if self._A is None:
            self._A = self.ts*self.ls
        return self._A

    @property
    def Ay(self) -> float:
        if self._Ay is None:
            self._Ay = self.A*(self.yb + self.ya)/2
        return self._Ay

    @property
    def Az(self) -> float:
        if self._Az is None:
            self._Az = self.A*(self.zb + self.za)/2
        return self._Az

    @property
    def Ayy(self) -> float:
        if self._Ayy is None:
            self._Ayy = self.A*(self.yb**2 + self.yb*self.ya + self.ya**2)/3
        return self._Ayy

    @property
    def Azz(self) -> float:
        if self._Azz is None:
            self._Azz = self.A*(self.zb**2 + self.zb*self.za + self.za**2)/3
        return self._Azz

    @property
    def Ayz(self) -> float:
        if self._Ayz is None:
            term1 = self.zb*self.yb + self.za*self.ya
            term2 = self.zb*self.ya + self.za*self.yb
            tmp = (term1 + term2/2)/3
            self._Ayz = self.A*tmp
        return self._Ayz

    def mpl_rectangle(self) -> Rectangle:
        thrad = radians(self.th)
        yo = self.ya+self.ts/2*sin(thrad)
        zo = self.za-self.ts/2*cos(thrad)
        rect = Rectangle((yo, zo), self.ls, self.ts, angle=self.th)
        return rect

    def __repr__(self) -> str:
        return '<WallSegment>'
