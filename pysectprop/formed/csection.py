from py2md.classes import MDTable
from ..general.generalsection import GeneralSection
from .. import config

class CSection(GeneralSection):
    hw = None
    wuf = None
    wlf = None
    ts = None
    rm = None
    def __init__(self, hw: float, wuf: float, wlf: float, ts: float,
                 rm: float, label: str=None):
        self.hw = hw
        self.wuf = wuf
        self.wlf = wlf
        self.ts = ts
        self.rm = rm
        y = [0.0, self.wlf, self.wlf, self.ts, self.ts, self.wuf, self.wuf, 0.0]
        z = [0.0, 0.0, self.ts, self.ts, self.hw-self.ts, self.hw-self.ts, self.hw, self.hw]
        if self.rm < self.ts/2:
            r = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        else:
            ri = self.rm-self.ts/2
            ro = self.rm+self.ts/2
            r = [ro, 0.0, 0.0, ri, ri, 0.0, 0.0, ro]
        super().__init__(y, z, r, label=label)
    def __repr__(self):
        if self.label is None:
            outstr = '<C-Section>'
        else:
            outstr = f'<C-Section {self.label:s}>'
        return outstr
    def __str__(self):
        mdstr = self.section_heading('C-Section')
        table = MDTable()
        table.add_column(f'h<sub>w</sub> ({config.lunit:s})', config.l1frm, data=[self.hw])
        table.add_column(f'w<sub>uf</sub> ({config.lunit:s})', config.l1frm, data=[self.wuf])
        table.add_column(f'w<sub>lf</sub> ({config.lunit:s})', config.l1frm, data=[self.wlf])
        table.add_column(f't<sub>s</sub> ({config.lunit:s})', config.l1frm, data=[self.ts])
        table.add_column(f'r<sub>m</sub> ({config.lunit:s})', config.l1frm, data=[self.rm])
        mdstr += str(table)
        mdstr += self.section_properties()
        return mdstr
    def _repr_markdown_(self):
        return self.__str__()
