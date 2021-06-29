from math import degrees
from py2md.classes import MDHeading, MDTable
from .generalsection import GeneralSection
from ..results.sectionresult import SectionResult
from .. import config
class MaterialSection(GeneralSection):
    material = None
    _EA = None
    _EAy = None
    _EAz = None
    _EAyy = None
    _EAzz = None
    _EAyz = None
    _EIyy = None
    _EIzz = None
    _EIyz = None
    _EIyp = None
    _EIzp = None
    def __init__(self, section, material):
        super().__init__(section.y, section.z, section.r, label=section.label)
        for k in section.__dict__:
            self.__dict__[k] = section.__dict__[k]
        self.material = material
    @property
    def EA(self):
        if self._EA is None:
            self._EA = self.material.E*self.A
        return self._EA
    @property
    def EAy(self):
        if self._EAy is None:
            self._EAy = self.material.E*self.Ay
        return self._EAy
    @property
    def EAz(self):
        if self._EAz is None:
            self._EAz = self.material.E*self.Az
        return self._EAz
    @property
    def EAyy(self):
        if self._EAyy is None:
            self._EAyy = self.material.E*self.Ayy
        return self._EAyy
    @property
    def EAzz(self):
        if self._EAzz is None:
            self._EAzz = self.material.E*self.Azz
        return self._EAzz
    @property
    def EAyz(self):
        if self._EAyz is None:
            self._EAyz = self.material.E*self.Ayz
        return self._EAyz
    @property
    def EIyy(self):
        if self._EIyy is None:
            self._EIyy = self.material.E*self.Iyy
        return self._EIyy
    @property
    def EIzz(self):
        if self._EIzz is None:
            self._EIzz = self.material.E*self.Izz
        return self._EIzz
    @property
    def EIyz(self):
        if self._EIyz is None:
            self._EIyz = self.material.E*self.Iyz
        return self._EIyz
    @property
    def EIyp(self):
        if self._EIyp is None:
            self._EIyp = self.material.E*self.Iyp
        return self._EIyp
    @property
    def EIzp(self):
        if self._EIzp is None:
            self._EIzp = self.material.E*self.Izp
        return self._EIzp
    def apply_load(self, loadcase, lctype, Fx, My, Mz):
        sectresult = SectionResult(self)
        sectresult.set_load(loadcase, lctype, Fx, My, Mz)
        return sectresult
    def __repr__(self):
        if self.label is None:
            outstr = '<MaterialSection>'
        else:
            outstr = f'<MaterialSection {self.label:s}>'
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
