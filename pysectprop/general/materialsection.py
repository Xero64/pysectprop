from math import degrees
from typing import TYPE_CHECKING, Any

from py2md.classes import MDHeading, MDTable

from .. import config
from ..results.sectionresult import SectionResult

if TYPE_CHECKING:
    from matplotlib.axes import Axes

    from .generalsection import GeneralSection
    from .hollowsection import HollowSection
    from .material import Material


class MaterialSection():
    section: 'GeneralSection | HollowSection' = None
    material: 'Material' = None
    label: str = None
    _EA: float = None
    _EAy: float = None
    _EAz: float = None
    _EAyy: float = None
    _EAzz: float = None
    _EAyz: float = None
    _EIyy: float = None
    _EIzz: float = None
    _EIyz: float = None
    _EIyp: float = None
    _EIzp: float = None

    def __init__(self, section: 'GeneralSection | HollowSection', material: 'Material',
                 label: str = None):
        self.section = section
        self.material = material
        self.label = label
        if self.label is None:
            self.label = self.section.label
        self.reset()

    def reset(self) -> None:
        for attr in self.__dict__:
            if attr[0] == '_':
                self.__dict__[attr] = None

    def mirror_y(self) -> None:
        self.section.mirror_y()
        self.reset()

    def mirror_z(self) -> None:
        self.section.mirror_z()
        self.reset()

    def translate(self, yt: float, zt: float) -> None:
        self.section.translate(yt, zt)
        self.reset()

    def rotate(self, theta: float) -> None:
        self.section.rotate(theta)
        self.reset()

    @property
    def EA(self) -> float:
        if self._EA is None:
            self._EA = self.material.E*self.section.A
        return self._EA

    @property
    def EAy(self) -> float:
        if self._EAy is None:
            self._EAy = self.material.E*self.section.Ay
        return self._EAy

    @property
    def EAz(self) -> float:
        if self._EAz is None:
            self._EAz = self.material.E*self.section.Az
        return self._EAz

    @property
    def cy(self) -> float:
        return self.section.cy

    @property
    def cz(self) -> float:
        return self.section.cz

    @property
    def EAyy(self) -> float:
        if self._EAyy is None:
            self._EAyy = self.material.E*self.section.Ayy
        return self._EAyy

    @property
    def EAzz(self) -> float:
        if self._EAzz is None:
            self._EAzz = self.material.E*self.section.Azz
        return self._EAzz

    @property
    def EAyz(self) -> float:
        if self._EAyz is None:
            self._EAyz = self.material.E*self.section.Ayz
        return self._EAyz

    @property
    def EIyy(self) -> float:
        if self._EIyy is None:
            self._EIyy = self.material.E*self.section.Iyy
        return self._EIyy

    @property
    def EIzz(self) -> float:
        if self._EIzz is None:
            self._EIzz = self.material.E*self.section.Izz
        return self._EIzz

    @property
    def EIyz(self) -> float:
        if self._EIyz is None:
            self._EIyz = self.material.E*self.section.Iyz
        return self._EIyz

    @property
    def thp(self) -> float:
        return self.section.thp

    @property
    def EIyp(self) -> float:
        if self._EIyp is None:
            self._EIyp = self.material.E*self.section.Iyp
        return self._EIyp

    @property
    def EIzp(self) -> float:
        if self._EIzp is None:
            self._EIzp = self.material.E*self.section.Izp
        return self._EIzp

    def plot(self, **kwargs: dict[str, Any]) -> 'Axes':
        return self.section.plot(**kwargs)

    def apply_load(self, loadcase: str, Fx: float, My: float, Mz: float,
                   limit: bool=False) -> SectionResult:
        sectresult = SectionResult(self)
        sectresult.set_load(loadcase, Fx, My, Mz, limit=limit)
        return sectresult

    def _repr_markdown_(self) -> str:
        funit = config.funit
        lunit = config.lunit
        l1frm = config.l1frm
        l2frm = config.l2frm
        l3frm = config.l3frm
        l4frm = config.l4frm
        angfrm = config.angfrm
        eiunit = f'{funit:s}.{lunit:s}<sup>2</sup>'
        mdstr = ''
        if self.label is None:
            head = 'Material Section Properties'
        else:
            head = f'Material Section Properties - {self.label:s}'
        heading = MDHeading(head, 3)
        mdstr += str(heading)
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
        eiunit = f'{funit:s}.{lunit:s}^2'
        outstr = ''
        if self.label is None:
            head = 'Material Section Properties'
        else:
            head = f'Material Section Properties - {self.label:s}'
        heading = MDHeading(head, 3)
        outstr += str(heading)
        table = MDTable()
        table.add_column(f'EA ({funit:s})', l2frm, data=[self.EA])
        table.add_column(f'EAy ({funit:s}.{lunit:s})', l3frm, data=[self.EAy])
        table.add_column(f'EAz ({funit:s}.{lunit:s})', l3frm, data=[self.EAz])
        table.add_column(f'cy ({lunit:s})', l1frm, data=[self.cy])
        table.add_column(f'cz ({lunit:s})', l1frm, data=[self.cz])
        table.add_column(f'EAyy ({eiunit:s})', l4frm, data=[self.EAyy])
        table.add_column(f'EAzz ({eiunit:s})', l4frm, data=[self.EAzz])
        table.add_column(f'EAyz ({eiunit:s})', l4frm, data=[self.EAyz])
        outstr += table.__str__()
        table = MDTable()
        table.add_column(f'EI_yy ({eiunit:s})', l4frm, data=[self.EIyy])
        table.add_column(f'EI_zz ({eiunit:s})', l4frm, data=[self.EIzz])
        table.add_column(f'EI_yz ({eiunit:s})', l4frm, data=[self.EIyz])
        table.add_column('th_p (deg)', angfrm,
                         data=[degrees(self.thp)])
        table.add_column(f'EI_yp ({eiunit:s})', l4frm, data=[self.EIyp])
        table.add_column(f'EI_zp ({eiunit:s})', l4frm, data=[self.EIzp])
        outstr += table.__str__()
        return outstr

    def __repr__(self) -> str:
        if self.label is None:
            outstr = '<MaterialSection>'
        else:
            outstr = f'<MaterialSection {self.label:s}>'
        return outstr
