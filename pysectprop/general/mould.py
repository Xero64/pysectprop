from math import sqrt  # , cos, asin
from typing import TYPE_CHECKING

from .arc import arc_from_points
from .compositesection import CompositeSection
from .generalsection import GeneralSection
from .materialsection import MaterialSection
from .point import Point

if TYPE_CHECKING:
    from .material import Material


class Mould(CompositeSection):
    y: list[float] = None
    z: list[float] = None
    r: list[float] = None
    _num: int = None
    _n: list[tuple[float, float]] = None

    def __init__(self, y: list[float], z: list[float], r: list[float],
                 label: str=None) -> None:
        self.y = y
        self.z = z
        self.r = r
        self.label = label
        self.sections = []

    @property
    def num(self) -> int:
        if self._num is None:
            self._num = len(self.y)
            if len(self.z) != self._num:
                raise ValueError('Mould z must be same length as y.')
            if len(self.r) != self._num:
                raise ValueError('Mould r must be same length as y.')
        return self._num

    @property
    def n(self) -> list[tuple[float, float]]:
        if self._n is None:
            self._n = []
            for i in range(self.num):
                if i == 0:
                    dyb = self.y[i+1] - self.y[i]
                    dzb = self.z[i+1] - self.z[i]
                    dsb = sqrt(dyb**2 + dzb**2)
                    nyb = -dzb/dsb
                    nzb = dyb/dsb
                    self._n.append((nyb, nzb))
                elif i == self.num - 1:
                    dya = self.y[i] - self.y[i-1]
                    dza = self.z[i] - self.z[i-1]
                    dsa = sqrt(dya**2 + dza**2)
                    nya = -dza/dsa
                    nza = dya/dsa
                    self._n.append((nya, nza))
                else:
                    pnta = Point(self.y[i-1], self.z[i-1])
                    pntb = Point(self.y[i], self.z[i])
                    pntc = Point(self.y[i+1], self.z[i+1])
                    arc = arc_from_points(pnta, pntb, pntc, 1.0)
                    if arc.sector.theta < 0.0:
                        sgn = -1.0
                    else:
                        sgn = 1.0
                    ny = sgn*(arc.pntf.y - arc.pntc.y)
                    nz = sgn*(arc.pntf.z - arc.pntc.z)
                    self._n.append((ny, nz, sgn))
        return self._n

    def add_ply(self, plyid: str, thick: float, offset: float,
                material: 'Material') -> MaterialSection:
        y = []
        z = []
        r = []
        for i in range(self.num):
            yi = self.y[i] + self.n[i][0]*offset
            zi = self.z[i] + self.n[i][1]*offset
            if i == 0 or i == self.num - 1 or self.r[i] is None:
                ri = 0.0
            else:
                ri = self.r[i] - self.n[i][2]*offset
            y.append(yi)
            z.append(zi)
            r.append(ri)
        for i in range(self.num-1, -1, -1):
            yi = self.y[i] + self.n[i][0]*(offset + thick)
            zi = self.z[i] + self.n[i][1]*(offset + thick)
            if i == 0 or i == self.num - 1 or self.r[i] is None:
                ri = 0.0
            else:
                ri = self.r[i] - self.n[i][2]*(offset + thick)
            y.append(yi)
            z.append(zi)
            r.append(ri)
        gensect = GeneralSection(y, z, r, label=str(plyid))
        matsect = MaterialSection(gensect, material)
        self.sections.append(matsect)
        return matsect
