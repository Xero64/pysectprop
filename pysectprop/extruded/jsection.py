from py2md.classes import MDTable
from ..general.generalsection import GeneralSection
from .. import config

class JSection(GeneralSection):
    hw = None
    tw = None
    wuf = None
    tuf = None
    wlf = None
    tlf = None
    hl = None
    tl = None

    def __init__(self, hw: float, tw: float, wuf: float, tuf: float,
                 wlf: float, tlf: float, hl: float=0.0, tl: float=0.0, label: str=None):

        self.hw = hw
        self.tw = tw
        self.wuf = wuf
        self.tuf = tuf
        self.wlf = wlf
        self.tlf = tlf
        self.hl = hl
        self.tl = tl

        pt1y = 0.0
        pt2y = self.wuf
        pt3y = self.wuf
        pt4y = pt3y - self.wuf/2 + self.tw/2
        pt5y = pt4y
        pt6y = pt5y -self.tw - self.wlf
        pt7y = pt6y
        pt8y = pt7y + self.tl
        pt9y = pt8y
        pt10y = pt9y + self.wlf - self.tl
        pt11y = pt10y
        pt12y = 0.0
        pt13y = pt1y

        pt1z = self.hw + self.tuf
        pt2z = pt1z
        pt3z = self.hw
        pt4z = pt3z
        pt5z = 0
        pt6z = pt5z
        pt7z = pt6z + self.tlf + self.hl
        pt8z = pt7z
        pt9z = self.tlf
        pt10z = pt9z
        pt11z = self.hw
        pt12z = pt11z
        pt13z = pt1z

        y = [pt1y, pt2y, pt3y, pt4y,
             pt5y, pt6y, pt7y, pt8y,
             pt9y, pt10y, pt11y, pt12y,
             pt13y]
        z = [pt1z, pt2z, pt3z, pt4z,
             pt5z, pt6z, pt7z, pt8z,
             pt9z, pt10z, pt11z, pt12z,
             pt13z]

        r = [0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0,
             0.0, 0.0, 0.0, 0.0,
             0.0]

        super().__init__(y, z, r, label=label)

    def __repr__(self):
        if self.label is None:
            outstr = '<J-Section>'
        else:
            outstr = f'<J-Section {self.label:s}>'
        return outstr
    def __str__(self):
        mdstr = self.section_heading('J-Section')
        table = MDTable()
        table.add_column(f'h<sub>w</sub> ({config.lunit:s})', config.l1frm, data=[self.hw])
        table.add_column(f't<sub>w</sub> ({config.lunit:s})', config.l1frm, data=[self.tw])
        table.add_column(f'w<sub>uf</sub> ({config.lunit:s})', config.l1frm, data=[self.wuf])
        table.add_column(f't<sub>uf</sub> ({config.lunit:s})', config.l1frm, data=[self.tuf])
        table.add_column(f'w<sub>lf</sub> ({config.lunit:s})', config.l1frm, data=[self.wlf])
        table.add_column(f't<sub>lf</sub> ({config.lunit:s})', config.l1frm, data=[self.tlf])
        if self.hl > 0.0:
            table.add_column(f'h<sub>l</sub> ({config.lunit:s})', config.l1frm, data=[self.hl])
        if self.tl > 0.0:
            table.add_column(f't<sub>l</sub> ({config.lunit:s})', config.l1frm, data=[self.tl])
        mdstr += str(table)
        mdstr += self.section_properties()
        return mdstr
    def _repr_markdown_(self):
        return self.__str__()
