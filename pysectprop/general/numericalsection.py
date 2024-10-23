from math import atan2, degrees, sqrt

from py2md.classes import MDHeading, MDTable

from .. import config


class NumericalSection():
    label: str = None
    _A: float = None
    _Ay: float = None
    _Az: float = None
    _Ayy: float = None
    _Azz: float = None
    _Ayz: float = None
    _cy: float = None
    _cz: float = None
    _Iyy: float = None
    _Izz: float = None
    _Iyz: float = None
    _Iav: float = None
    _Idf: float = None
    _Isq: float = None
    _cos2thp: float = None
    _sin2thp: float = None
    _thp: float = None
    _Iyp: float = None
    _Izp: float = None

    def __init__(self, label: str=None) -> None:
        if label is not None:
            self.label = label

    def check_area(self) -> None:
        pass

    def reset(self) -> None:
        for attr in self.__dict__:
            if attr[0] == '_':
                self.__dict__[attr] = None
        self.check_area()

    @property
    def A(self) -> float:
        if self._A is None:
            raise ValueError('self._A needs to be specified.')
        return self._A

    @property
    def Ay(self) -> float:
        if self._Ay is None:
            raise ValueError('self._Ay needs to be specified.')
        return self._Ay

    @property
    def Az(self) -> float:
        if self._Az is None:
            raise ValueError('self._Az needs to be specified.')
        return self._Az

    @property
    def Ayy(self) -> float:
        if self._Ayy is None:
            raise ValueError('self._Ayz needs to be specified.')
        return self._Ayy

    @property
    def Azz(self) -> float:
        if self._Azz is None:
            raise ValueError('self._Ayz needs to be specified.')
        return self._Azz

    @property
    def Ayz(self) -> float:
        if self._Ayz is None:
            raise ValueError('self._Ayz needs to be specified.')
        return self._Ayz

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
    def Iav(self) -> float:
        if self._Iav is None:
            self._Iav = (self.Iyy + self.Izz)/2
        return self._Iav

    @property
    def Idf(self) -> float:
        if self._Idf is None:
            self._Idf = (self.Iyy - self.Izz)/2
        return self._Idf

    @property
    def Isq(self) -> float:
        if self._Isq is None:
            self._Isq = sqrt(self.Idf**2 + self.Iyz**2)
        return self._Isq

    @property
    def cos2thp(self) -> float:
        if self._cos2thp is None:
            if self.Isq == 0.0:
                self._cos2thp = 1.0
            else:
                self._cos2thp = self.Idf/self.Isq
            if abs(self.Idf/self.Iav) < 1e-12:
                self._cos2thp = 0.0
        return self._cos2thp

    @property
    def sin2thp(self) -> float:
        if self._sin2thp is None:
            if self.Isq == 0.0:
                self._sin2thp = 0.0
            else:
                self._sin2thp = -self.Iyz/self.Isq
            if abs(self.Iyz/self.Iav) < 1e-12:
                self._sin2thp = 0.0
        return self._sin2thp

    @property
    def thp(self) -> float:
        if self._thp is None:
            self._thp = 0.5*atan2(self.sin2thp, self.cos2thp)
        return self._thp

    @property
    def Iyp(self) -> float:
        if self._Iyp is None:
            self._Iyp = self.Iav + self.Idf*self.cos2thp - self.Iyz*self.sin2thp
        return self._Iyp

    @property
    def Izp(self) -> float:
        if self._Izp is None:
            self._Izp = self.Iav - self.Idf*self.cos2thp + self.Iyz*self.sin2thp
        return self._Izp

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
            mdstr += self.section_heading('Numerical Section')
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
            mdstr += table.__str__()
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
            mdstr += table.__str__()
        return mdstr

    def _repr_markdown_(self) -> str:
        return self.section_properties(nohead=False, outtype='md')

    def __str__(self) -> str:
        return self.section_properties(nohead=False, outtype=str)

    def __repr__(self) -> str:
        if self.label is None:
            outstr = '<NumericalSection>'
        else:
            outstr = f'<NumericalSection {self.label:s}>'
        return outstr
