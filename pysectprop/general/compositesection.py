from math import atan2, degrees, sqrt
from typing import TYPE_CHECKING

from matplotlib.collections import PatchCollection
from matplotlib.patches import Patch, PathPatch
from matplotlib.path import Path
from matplotlib.pyplot import figure, rcParams
from py2md.classes import MDHeading, MDTable

from .. import config
from ..results.sectionresult import SectionResult
from .numericalsection import NumericalSection

if TYPE_CHECKING:
    from matplotlib.axes import Axes

    from .material import Material
    from .materialsection import MaterialSection


class CompositeSection():
    sections: list['MaterialSection'] = None
    label: str = None
    _EA: float = None
    _EAy: float = None
    _EAz: float = None
    _cy: float = None
    _cz: float = None
    _EAyy: float = None
    _EAzz: float = None
    _EAyz: float = None
    _EIyy: float = None
    _EIzz: float = None
    _EIyz: float = None
    _EIav: float = None
    _EIdf: float = None
    _EIsq: float = None
    _cos2thp: float = None
    _sin2thp: float = None
    _thp: float = None
    _EIyp: float = None
    _EIzp: float = None

    def __init__(self, sections: list['MaterialSection'], label: str=None) -> None:
        self.sections = sections
        self.label = label

    def reset(self) -> None:
        for attr in self.__dict__:
            if attr[0] == '_':
                self.__dict__[attr] = None

    def mirror_y(self) -> None:
        for section in self.sections:
            section.mirror_y()
        self.reset()

    def mirror_z(self) -> None:
        for section in self.sections:
            section.mirror_z()
        self.reset()

    def translate(self, yt: float, zt: float) -> None:
        for section in self.sections:
            section.translate(yt, zt)
        self.reset()

    def rotate(self, theta: float) -> None:
        for section in self.sections:
            section.rotate(theta)
        self.reset()

    @property
    def EA(self) -> float:
        if self._EA is None:
            self._EA = 0.0
            for section in self.sections:
                self._EA += section.EA
        return self._EA

    @property
    def EAy(self) -> float:
        if self._EAy is None:
            self._EAy = 0.0
            for section in self.sections:
                self._EAy += section.EAy
        return self._EAy

    @property
    def EAz(self) -> float:
        if self._EAz is None:
            self._EAz = 0.0
            for section in self.sections:
                self._EAz += section.EAz
        return self._EAz

    @property
    def cy(self) -> float:
        if self._cy is None:
            self._cy = self.EAy/self.EA
        return self._cy

    @property
    def cz(self) -> float:
        if self._cz is None:
            self._cz = self.EAz/self.EA
        return self._cz

    @property
    def EAyy(self) -> float:
        if self._EAyy is None:
            self._EAyy = 0.0
            for section in self.sections:
                self._EAyy += section.EAyy
        return self._EAyy

    @property
    def EAzz(self) -> float:
        if self._EAzz is None:
            self._EAzz = 0.0
            for section in self.sections:
                self._EAzz += section.EAzz
        return self._EAzz

    @property
    def EAyz(self) -> float:
        if self._EAyz is None:
            self._EAyz = 0.0
            for section in self.sections:
                self._EAyz += section.EAyz
        return self._EAyz

    @property
    def EIyy(self) -> float:
        if self._EIyy is None:
            self._EIyy = self.EAzz - self.EA*self.cz**2
        return self._EIyy

    @property
    def EIzz(self) -> float:
        if self._EIzz is None:
            self._EIzz = self.EAyy - self.EA*self.cy**2
        return self._EIzz

    @property
    def EIyz(self) -> float:
        if self._EIyz is None:
            self._EIyz = self.EAyz - self.EA*self.cy*self.cz
        return self._EIyz

    @property
    def EIav(self) -> float:
        if self._EIav is None:
            self._EIav = (self.EIyy + self.EIzz)/2
        return self._EIav

    @property
    def EIdf(self) -> float:
        if self._EIdf is None:
            self._EIdf = (self.EIyy - self.EIzz)/2
        return self._EIdf

    @property
    def EIsq(self) -> float:
        if self._EIsq is None:
            self._EIsq = sqrt(self.EIdf**2 + self.EIyz**2)
        return self._EIsq

    @property
    def cos2thp(self) -> float:
        if self._cos2thp is None:
            self._cos2thp = self.EIdf/self.EIsq
            if abs(self.EIdf/self.EIav) < 1e-12:
                self._cos2thp = 0.0
        return self._cos2thp

    @property
    def sin2thp(self) -> float:
        if self._sin2thp is None:
            self._sin2thp = -self.EIyz/self.EIsq
            if abs(self.EIyz/self.EIav) < 1e-12:
                self._sin2thp = 0.0
        return self._sin2thp

    @property
    def thp(self) -> float:
        if self._thp is None:
            self._thp = 0.5*atan2(self.sin2thp, self.cos2thp)
        return self._thp

    @property
    def EIyp(self) -> float:
        if self._EIyp is None:
            self._EIyp = self.EIav + self.EIdf*self.cos2thp - self.EIyz*self.sin2thp
        return self._EIyp

    @property
    def EIzp(self) -> float:
        if self._EIzp is None:
            self._EIzp = self.EIav - self.EIdf*self.cos2thp + self.EIyz*self.sin2thp
        return self._EIzp

    def plot(self, ax: 'Axes'=None, legloc: str='best') -> 'Axes':
        if ax is None:
            fig = figure(figsize=(12, 8))
            ax = fig.gca()
        ax.set_aspect('equal')
        numsect = len(self.sections)
        prop_cycle = rcParams['axes.prop_cycle']
        propcolors = prop_cycle.by_key()['color']
        colors = []
        while len(colors) < numsect:
            colors.extend(propcolors)
        patches = []
        y, z = [], []
        legel = []
        for i, section in enumerate(self.sections):
            verts = []
            codes = []
            for obj in section.section.path:
                obj.add_path(verts, codes)
            path = Path(verts, codes)
            patch = PathPatch(path)
            y += section.section.y
            z += section.section.z
            patches.append(patch)
            label = ''
            if section.label is not None:
                label = section.label
            legel.append(Patch(facecolor=colors[i], alpha=0.6, label=label))
        p = PatchCollection(patches, alpha=0.6)
        p.set_facecolor(colors)
        ax.add_collection(p)
        ax.set_xlim(min(y), max(y))
        ax.set_ylim(min(z), max(z))
        ax.legend(handles=legel, loc=legloc)
        return ax

    def apply_load(self, loadcase, Fx, My, Mz,
                   limit: bool=False) -> list[SectionResult]:
        sectresults = []
        for section in self.sections:
            sectresult = SectionResult(section, totalsection=self)
            sectresult.set_load(loadcase, Fx, My, Mz, limit=limit)
            sectresults.append(sectresult)
        return sectresults

    def _repr_markdown_(self) -> str:
        funit = config.funit
        lunit = config.lunit
        l1frm = config.l1frm
        l2frm = config.l2frm
        l3frm = config.l3frm
        l4frm = config.l4frm
        angfrm = config.angfrm
        eiunit = f'{funit:s}.{lunit:s}<sup>2</sup>'
        if self.label is None:
            head = 'Composite Section Properties'
        else:
            head = f'Composite Section Properties - {self.label:s}'
        heading = MDHeading(head, 3)
        mdstr = heading._repr_markdown_()
        table = MDTable()
        table.add_column(f'EA ({funit:s})', l2frm, data=[self.EA])
        table.add_column(f'EAy ({funit:s}.{lunit:s})', l3frm, data=[self.EAy])
        table.add_column(f'EAz ({funit:s}.{lunit:s})', l3frm, data=[self.EAz])
        table.add_column(f'cy ({lunit:s})', l1frm, data=[self.cy])
        table.add_column(f'cz ({lunit:s})', l1frm, data=[self.cz])
        table.add_column(f'EAyy ({eiunit:s})', l4frm, data=[self.EAyy])
        table.add_column(f'EAzz ({eiunit:s})', l4frm, data=[self.EAzz])
        table.add_column(f'EAyz ({eiunit:s})', l4frm, data=[self.EAyz])
        mdstr += table._repr_markdown_()
        table = MDTable()
        table.add_column(f'EI<sub>yy</sub> ({eiunit:s})', l4frm, data=[self.EIyy])
        table.add_column(f'EI<sub>zz</sub> ({eiunit:s})', l4frm, data=[self.EIzz])
        table.add_column(f'EI<sub>yz</sub> ({eiunit:s})', l4frm, data=[self.EIyz])
        table.add_column('&theta;<sub>p</sub> (&deg;)', angfrm,
                         data=[degrees(self.thp)])
        table.add_column(f'EI<sub>yp</sub> ({eiunit:s})', l4frm, data=[self.EIyp])
        table.add_column(f'EI<sub>zp</sub> ({eiunit:s})', l4frm, data=[self.EIzp])
        mdstr += table._repr_markdown_()
        return mdstr

    def __str__(self) -> str:
        funit = config.funit
        lunit = config.lunit
        l1frm = config.l1frm
        l2frm = config.l2frm
        l3frm = config.l3frm
        l4frm = config.l4frm
        angfrm = config.angfrm
        eiunit = f'{funit:s}.{lunit:s}<sup>2</sup>'
        if self.label is None:
            head = 'Composite Section Properties'
        else:
            head = f'Composite Section Properties - {self.label:s}'
        heading = MDHeading(head, 3)
        mdstr = heading.__str__()
        table = MDTable()
        table.add_column(f'EA ({funit:s})', l2frm, data=[self.EA])
        table.add_column(f'EAy ({funit:s}.{lunit:s})', l3frm, data=[self.EAy])
        table.add_column(f'EAz ({funit:s}.{lunit:s})', l3frm, data=[self.EAz])
        table.add_column(f'cy ({lunit:s})', l1frm, data=[self.cy])
        table.add_column(f'cz ({lunit:s})', l1frm, data=[self.cz])
        table.add_column(f'EAyy ({eiunit:s})', l4frm, data=[self.EAyy])
        table.add_column(f'EAzz ({eiunit:s})', l4frm, data=[self.EAzz])
        table.add_column(f'EAyz ({eiunit:s})', l4frm, data=[self.EAyz])
        mdstr += table.__str__()
        table = MDTable()
        table.add_column(f'EI_yy ({eiunit:s})', l4frm, data=[self.EIyy])
        table.add_column(f'EI_zz ({eiunit:s})', l4frm, data=[self.EIzz])
        table.add_column(f'EI_yz ({eiunit:s})', l4frm, data=[self.EIyz])
        table.add_column('th_p (deg)', angfrm, data=[degrees(self.thp)])
        table.add_column(f'EI_yp ({eiunit:s})', l4frm, data=[self.EIyp])
        table.add_column(f'EI_zp ({eiunit:s})', l4frm, data=[self.EIzp])
        mdstr += table.__str__()
        return mdstr

    def __repr__(self) -> str:
        if self.label is None:
            outstr = '<CompositeSection>'
        else:
            outstr = f'<CompositeSection {self.label:s}>'
        return outstr

def normalise_composite_section(compsect: CompositeSection,
                                material: 'Material') -> str:

    numsect = NumericalSection(compsect.label)
    numsect._A = compsect.EA/material.E
    numsect._Ay = compsect.EAy/material.E
    numsect._Az = compsect.EAz/material.E
    numsect._Ayy = compsect.EAyy/material.E
    numsect._Azz = compsect.EAzz/material.E
    numsect._Ayz = compsect.EAyz/material.E

    return numsect
