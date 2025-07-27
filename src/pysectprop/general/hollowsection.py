from typing import TYPE_CHECKING

from matplotlib.patches import PathPatch
from matplotlib.path import Path
from matplotlib.pyplot import figure

from .generalsection import GeneralSection
from .numericalsection import NumericalSection

if TYPE_CHECKING:
    from matplotlib.axes import Axes

    from .point import Point


class Hole(GeneralSection):

    def check_area(self, display=False) -> None:
        self._A = None
        if self.A > 0.0:
            if display:
                print('Reversed coordinates.')
            self.y.reverse()
            self.z.reverse()
            self.r.reverse()
            self.generate_path()
        self._A = None

class HollowSection(NumericalSection):
    outer: GeneralSection = None
    inner: Hole = None

    def __init__(self, outer: GeneralSection, inner: Hole,
                 label: str=None) -> None:
        self.outer = outer
        self.inner = inner
        if not isinstance(self.inner, Hole) and isinstance(self.inner, GeneralSection):
            self.inner.__class__ = Hole
        self.inner.reset()
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
    def pnts(self) -> list['Point']:
        return self.outer.pnts

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

    def plot(self, ax: 'Axes | None' = None) -> 'Axes':
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

    def _repr_markdown_(self) -> str:
        mdstr = self.section_heading('Hollow Section')
        mdstr += self.section_properties(outtype='md')
        return mdstr

    def __str__(self) -> str:
        mdstr = self.section_heading('Hollow Section')
        mdstr += self.section_properties(outtype=str)
        return mdstr

    def __repr__(self) -> str:
        if self.label is None:
            outstr = '<HollowSection>'
        else:
            outstr = f'<HollowSection {self.label:s}>'
        return outstr
