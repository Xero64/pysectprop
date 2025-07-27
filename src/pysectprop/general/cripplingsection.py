from math import degrees
from typing import TYPE_CHECKING

from py2md.classes import MDHeading, MDTable

from .. import config
from .thinwalledsection import ThinWalledSection

if TYPE_CHECKING:
    from .material import Material

class CripplingSection(ThinWalledSection):
    material: 'Material' = None
    coef: float = None
    cnef: float = None
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

    def __init__(self, section: ThinWalledSection, material: 'Material',
                 coef: float, cnef: float) -> None:
        if isinstance(section, ThinWalledSection):
            super().__init__(section.y, section.z, section.t, label=section.label)
            for k in section.__dict__:
                self.__dict__[k] = section.__dict__[k]
        self.material = material
        self.coef = coef
        self.cnef = cnef

    @property
    def EA(self) -> float:
        if self._EA is None:
            self._EA = self.material.Ec*self.A
        return self._EA

    @property
    def EAy(self) -> float:
        if self._EAy is None:
            self._EAy = self.material.Ec*self.Ay
        return self._EAy

    @property
    def EAz(self) -> float:
        if self._EAz is None:
            self._EAz = self.material.Ec*self.Az
        return self._EAz

    @property
    def EAyy(self) -> float:
        if self._EAyy is None:
            self._EAyy = self.material.Ec*self.Ayy
        return self._EAyy

    @property
    def EAzz(self) -> float:
        if self._EAzz is None:
            self._EAzz = self.material.Ec*self.Azz
        return self._EAzz

    @property
    def EAyz(self) -> float:
        if self._EAyz is None:
            self._EAyz = self.material.Ec*self.Ayz
        return self._EAyz

    @property
    def EIyy(self) -> float:
        if self._EIyy is None:
            self._EIyy = self.material.Ec*self.Iyy
        return self._EIyy

    @property
    def EIzz(self) -> float:
        if self._EIzz is None:
            self._EIzz = self.material.Ec*self.Izz
        return self._EIzz

    @property
    def EIyz(self) -> float:
        if self._EIyz is None:
            self._EIyz = self.material.Ec*self.Iyz
        return self._EIyz

    @property
    def EIyp(self) -> float:
        if self._EIyp is None:
            self._EIyp = self.material.Ec*self.Iyp
        return self._EIyp

    @property
    def EIzp(self) -> float:
        if self._EIzp is None:
            self._EIzp = self.material.Ec*self.Izp
        return self._EIzp

    def _repr_markdown_(self) -> str:
        funit = config.funit
        lunit = config.lunit
        sunit = config.sunit
        l1frm = config.l1frm
        l2frm = config.l2frm
        l3frm = config.l3frm
        l4frm = config.l4frm
        angfrm = config.angfrm
        eiunit = f'{funit:s}.{lunit:s}<sup>2</sup>'
        if self.label is None:
            head = 'Crippling Section Properties'
        else:
            head = f'Crippling Section Properties - {self.label:s}'
        heading = MDHeading(head, 3)
        mdstr = str(heading)
        table = MDTable()
        table.add_column(f'EA ({funit:s})', l2frm, data=[self.EA])
        table.add_column(f'EAy ({funit:s}.{lunit:s})', l3frm, data=[self.EAy])
        table.add_column(f'EAz ({funit:s}.{lunit:s})', l3frm, data=[self.EAz])
        table.add_column(f'cy ({lunit:s})', l1frm, data=[self.cy])
        table.add_column(f'cz ({lunit:s})', l1frm, data=[self.cy])
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
        Ec = self.material.Ec
        Fcy = self.material.Fcy
        table = MDTable()
        table.add_column(f'E<sub>c</sub> ({sunit:s})', '.0f', data=[self.material.Ec])
        table.add_column(f'F<sub>cy</sub> ({sunit:s})', '.0f', data=[self.material.Fcy])
        table.add_column('C<sub>oef</sub>', '.3f', data=[self.coef])
        table.add_column('C<sub>nef</sub>', '.3f', data=[self.cnef])
        mdstr += table._repr_markdown_()
        table = MDTable()
        table.add_column('#', '')
        table.add_column(f'b ({lunit:s})', '')
        table.add_column(f't ({lunit:s})', '')
        table.add_column('C', '')
        table.add_column(f'A ({lunit:s}<sup>2</sup>)', '.1f')
        table.add_column(f'F ({sunit:s})', '.1f')
        table.add_column(f'P ({funit:s})', '.0f')
        Acc_tot = 0.0
        Pcc_tot = 0.0
        frm = '{:' + l1frm + '}'
        for ind, seg in enumerate(self.segs):
            b = seg.ls
            t = seg.ts
            if seg.is_oef():
                cef = self.coef
                Fcc = min([(Ec*Fcy)**0.5*cef/(b/t)**0.75, Fcy])
            if seg.is_nef():
                cef = self.cnef
                Fcc = min([(Ec*Fcy)**0.5*cef/(b/2/t)**0.75, Fcy])
            Acc = seg.A
            Pcc = Fcc*Acc
            Pcc_tot += Pcc
            Acc_tot += Acc
            data = [ind, frm.format(b), frm.format(t), cef, Acc, Fcc, Pcc]
            table.add_row(data)
        Fcc_tot = Pcc_tot/Acc_tot
        table.add_row(['Total', '-', '-', '-', Acc_tot, Fcc_tot, Pcc_tot])
        mdstr += table._repr_markdown_()
        return mdstr

    def __str__(self) -> str:
        funit = config.funit
        lunit = config.lunit
        sunit = config.sunit
        l1frm = config.l1frm
        l2frm = config.l2frm
        l3frm = config.l3frm
        l4frm = config.l4frm
        angfrm = config.angfrm
        eiunit = f'{funit:s}.{lunit:s}^2'
        if self.label is None:
            head = 'Crippling Section Properties'
        else:
            head = f'Crippling Section Properties - {self.label:s}'
        heading = MDHeading(head, 3)
        outstr = str(heading)
        table = MDTable()
        table.add_column(f'EA ({funit:s})', l2frm, data=[self.EA])
        table.add_column(f'EAy ({funit:s}.{lunit:s})', l3frm, data=[self.EAy])
        table.add_column(f'EAz ({funit:s}.{lunit:s})', l3frm, data=[self.EAz])
        table.add_column(f'cy ({lunit:s})', l1frm, data=[self.cy])
        table.add_column(f'cz ({lunit:s})', l1frm, data=[self.cy])
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
        Ec = self.material.Ec
        Fcy = self.material.Fcy
        table = MDTable()
        table.add_column(f'E_c ({sunit:s})', '.0f', data=[self.material.Ec])
        table.add_column(f'F_cy ({sunit:s})', '.0f', data=[self.material.Fcy])
        table.add_column('C_oef', '.3f', data=[self.coef])
        table.add_column('C_nef', '.3f', data=[self.cnef])
        outstr += table.__str__()
        table = MDTable()
        table.add_column('#', '')
        table.add_column(f'b ({lunit:s})', '')
        table.add_column(f't ({lunit:s})', '')
        table.add_column('C', '')
        table.add_column(f'A ({lunit:s}^2)', '.1f')
        table.add_column(f'F ({sunit:s})', '.1f')
        table.add_column(f'P ({funit:s})', '.0f')
        Acc_tot = 0.0
        Pcc_tot = 0.0
        frm = '{:' + l1frm + '}'
        for ind, seg in enumerate(self.segs):
            b = seg.ls
            t = seg.ts
            if seg.is_oef():
                cef = self.coef
                Fcc = min([(Ec*Fcy)**0.5*cef/(b/t)**0.75, Fcy])
            if seg.is_nef():
                cef = self.cnef
                Fcc = min([(Ec*Fcy)**0.5*cef/(b/2/t)**0.75, Fcy])
            Acc = seg.A
            Pcc = Fcc*Acc
            Pcc_tot += Pcc
            Acc_tot += Acc
            data = [ind, frm.format(b), frm.format(t), cef, Acc, Fcc, Pcc]
            table.add_row(data)
        Fcc_tot = Pcc_tot/Acc_tot
        table.add_row(['Total', '', '', '', Acc_tot, Fcc_tot, Pcc_tot])
        outstr += table.__str__()
        return outstr

    def __repr__(self) -> str:
        if self.label is None:
            outstr = '<CripplingSection>'
        else:
            outstr = f'<CripplingSection {self.label:s}>'
        return outstr
