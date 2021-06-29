from math import cos, sin, pi, atan, degrees
from matplotlib.pyplot import figure
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Patch
from matplotlib.collections import PatchCollection
from matplotlib.pyplot import rcParams
from py2md.classes import MDHeading, MDTable
from ..results.sectionresult import SectionResult
from .. import config

class CompositeSection(object):
    sections = None
    label: str = None
    _EA = None
    _EAy = None
    _EAz = None
    _cy = None
    _cz = None
    _EAyy = None
    _EAzz = None
    _EAyz = None
    _EIyy = None
    _EIzz = None
    _EIyz = None
    _θp = None
    _EIyp = None
    _EIzp = None
    def __init__(self, sections: list, label: str=None):
        self.sections = sections
        self.label = label
    def reset(self):
        self._EA = None
        self._EAy = None
        self._EAz = None
        self._cy = None
        self._cz = None
        self._EAyy = None
        self._EAzz = None
        self._EAyz = None
        self._EIyy = None
        self._EIzz = None
        self._EIyz = None
        self._θp = None
        self._EIyp = None
        self._EIzp = None
    @property
    def EA(self):
        if self._EA is None:
            self._EA = 0.0
            for section in self.sections:
                self._EA += section.EA
        return self._EA
    @property
    def EAy(self):
        if self._EAy is None:
            self._EAy = 0.0
            for section in self.sections:
                self._EAy += section.EAy
        return self._EAy
    @property
    def EAz(self):
        if self._EAz is None:
            self._EAz = 0.0
            for section in self.sections:
                self._EAz += section.EAz
        return self._EAz
    @property
    def cy(self):
        if self._cy is None:
            self._cy = self.EAy/self.EA
        return self._cy
    @property
    def cz(self):
        if self._cz is None:
            self._cz = self.EAz/self.EA
        return self._cz
    @property
    def EAyy(self):
        if self._EAyy is None:
            self._EAyy = 0.0
            for section in self.sections:
                self._EAyy += section.EAyy
        return self._EAyy
    @property
    def EAzz(self):
        if self._EAzz is None:
            self._EAzz = 0.0
            for section in self.sections:
                self._EAzz += section.EAzz
        return self._EAzz
    @property
    def EAyz(self):
        if self._EAyz is None:
            self._EAyz = 0.0
            for section in self.sections:
                self._EAyz += section.EAyz
        return self._EAyz
    @property
    def EIyy(self):
        if self._EIyy is None:
            self._EIyy = self.EAzz-self.EA*self.cz**2
        return self._EIyy
    @property
    def EIzz(self):
        if self._EIzz is None:
            self._EIzz = self.EAyy-self.EA*self.cy**2
        return self._EIzz
    @property
    def EIyz(self):
        if self._EIyz is None:
            self._EIyz = self.EAyz-self.EA*self.cy*self.cz
        return self._EIyz
    @property
    def θp(self):
        if self._θp is None:
            tol = 1e-12
            if abs(2*self.EIyz) < tol:
                self._θp = 0.0
            elif abs(self.EIzz-self.EIyy) < tol:
                self._θp = pi/4
            else:
                self._θp = atan(2*self.EIyz/(self.EIzz-self.EIyy))/2
        return self._θp
    @property
    def EIyp(self):
        if self._EIyp is None:
            c = cos(self.θp)
            s = sin(self.θp)
            self._EIyp = self.EIyy*c**2+self.EIzz*s**2-2*self.EIyz*c*s
        return self._EIyp
    @property
    def EIzp(self):
        if self._EIzp is None:
            c = cos(self.θp)
            s = sin(self.θp)
            self._EIzp = self.EIyy*s**2+self.EIzz*c**2+2*self.EIyz*c*s
        return self._EIzp
    def plot(self, ax=None, legloc: str='best'):
        if ax is None:
            fig = figure(figsize=(12, 8))
            ax = fig.gca()
        ax.set_aspect('equal')
        prop_cycle = rcParams['axes.prop_cycle']
        colors = prop_cycle.by_key()['color']
        patches = []
        y, z = [], []
        legel = []
        for i, section in enumerate(self.sections):
            verts = []
            codes = []
            for obj in section.path:
                obj.add_path(verts, codes)
            path = Path(verts, codes)
            patch = PathPatch(path)
            y += section.y
            z += section.z
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
    def apply_load(self, loadcase, Fx, My, Mz, limit: bool=False):
        sectresults = []
        for section in self.sections:
            sectresult = SectionResult(section, totalsection=self)
            sectresult.set_load(loadcase, Fx, My, Mz, limit=limit)
            sectresults.append(sectresult)
        return sectresults
    def __repr__(self):
        if self.label is None:
            outstr = '<CompositeSection>'
        else:
            outstr = f'<CompositeSection {self.label:s}>'
        return outstr
    def __str__(self):
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
        mdstr = str(heading)
        table = MDTable()
        table.add_column(f'EA ({funit:s})', l2frm, data=[self.EA])
        table.add_column(f'EAy ({funit:s}.{lunit:s})', l3frm, data=[self.EAy])
        table.add_column(f'EAz ({funit:s}.{lunit:s})', l3frm, data=[self.EAz])
        table.add_column(f'cy ({lunit:s})', l1frm, data=[self.cy])
        table.add_column(f'cz ({lunit:s})', l1frm, data=[self.cz])
        table.add_column(f'EAyy ({eiunit:s})', l4frm, data=[self.EAyy])
        table.add_column(f'EAzz ({eiunit:s})', l4frm, data=[self.EAzz])
        table.add_column(f'EAyz ({eiunit:s})', l4frm, data=[self.EAyz])
        mdstr += str(table)
        table = MDTable()
        table.add_column(f'EI<sub>yy</sub> ({eiunit:s})', l4frm, data=[self.EIyy])
        table.add_column(f'EI<sub>zz</sub> ({eiunit:s})', l4frm, data=[self.EIzz])
        table.add_column(f'EI<sub>yz</sub> ({eiunit:s})', l4frm, data=[self.EIyz])
        table.add_column('&theta;<sub>p</sub> (&deg;)', angfrm, data=[degrees(self.θp)])
        table.add_column(f'EI<sub>yp</sub> ({eiunit:s})', l4frm, data=[self.EIyp])
        table.add_column(f'EI<sub>zp</sub> ({eiunit:s})', l4frm, data=[self.EIzp])
        mdstr += str(table)
        return mdstr
    def _repr_markdown_(self):
        return self.__str__()

def normalise_composite_section(compsect: CompositeSection, material):
    lunit = config.lunit
    l1frm = config.l1frm
    l2frm = config.l2frm
    l3frm = config.l3frm
    l4frm = config.l4frm
    angfrm = config.angfrm
    E = material.E
    # Needs material data added to this output for reference.
    if compsect.label is None:
        head = 'Normalised Composite Section Properties'
    else:
        head = f'Normalised Composite Section Properties - {compsect.label:s}'
    heading = MDHeading(head, 3)
    mdstr = str(heading)
    table = MDTable()
    table.add_column(f'A ({lunit:s}<sup>2</sup>)', l2frm, data=[compsect.EA/E])
    table.add_column(f'Ay ({lunit:s}<sup>3</sup>)', l3frm, data=[compsect.EAy/E])
    table.add_column(f'Az ({lunit:s}<sup>3</sup>)', l3frm, data=[compsect.EAz/E])
    table.add_column(f'cy ({lunit:s})', l1frm, data=[compsect.cy])
    table.add_column(f'cz ({lunit:s})', l1frm, data=[compsect.cz])
    table.add_column(f'Ayy ({lunit:s}<sup>4</sup>)', l4frm, data=[compsect.EAyy/E])
    table.add_column(f'Azz ({lunit:s}<sup>4</sup>)', l4frm, data=[compsect.EAzz/E])
    table.add_column(f'Ayz ({lunit:s}<sup>4</sup>)', l4frm, data=[compsect.EAyz/E])
    mdstr += str(table)
    table = MDTable()
    table.add_column(f'I<sub>yy</sub> ({lunit:s}<sup>4</sup>)', l4frm, data=[compsect.EIyy/E])
    table.add_column(f'I<sub>zz</sub> ({lunit:s}<sup>4</sup>)', l4frm, data=[compsect.EIzz/E])
    table.add_column(f'I<sub>yz</sub> ({lunit:s}<sup>4</sup>)', l4frm, data=[compsect.EIyz/E])
    table.add_column('&theta;<sub>p</sub> (&deg;)', angfrm, data=[degrees(compsect.θp)])
    table.add_column(f'I<sub>yp</sub> ({lunit:s}<sup>4</sup>)', l4frm, data=[compsect.EIyp/E])
    table.add_column(f'I<sub>zp</sub> ({lunit:s}<sup>4</sup>)', l4frm, data=[compsect.EIzp/E])
    mdstr += str(table)
    return mdstr
