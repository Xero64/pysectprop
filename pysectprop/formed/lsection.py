from py2md.classes import MDTable
from ..general.generalsection import GeneralSection
from ..general.thinwalledsection import ThinWalledSection
from .. import config

class LSection(GeneralSection):
    hw = None
    wf = None
    ts = None
    rm = None
    hl = None
    def __init__(self, hw: float, wf: float, ts: float, rm: float,
                 hl: float=0.0, label: str=None):
        self.hw = hw
        self.wf = wf
        self.ts = ts
        self.rm = rm
        self.hl = hl
        if self.hl == 0.0:
            y = [0.0, self.wf, self.wf, self.ts, self.ts, 0.0]
            z = [0.0, 0.0, self.ts, self.ts, self.hw, self.hw]
            r = [self.rm+self.ts/2, 0.0, 0.0, self.rm-self.ts/2, 0.0, 0.0]
        else:
            y = [0.0, self.wf, self.wf, self.wf-self.ts, self.wf-self.ts, self.ts, self.ts, 0.0]
            z = [0.0, 0.0, self.hl, self.hl, self.ts, self.ts, self.hw, self.hw]
            r = [self.rm+self.ts/2, self.rm+self.ts/2, 0.0, 0.0,
                 self.rm-self.ts/2, self.rm-self.ts/2, 0.0, 0.0]
        super().__init__(y, z, r, label=label)
    def to_thin_walled(self):
        if self.hl == 0.0:
            y = [self.ts/2, self.ts/2, self.wf]
            z = [self.hw, self.ts/2, self.ts/2]
            t = [self.ts, self.ts]
        else:
            y = [self.ts/2, self.ts/2, self.wf-self.ts/2, self.wf-self.ts/2]
            z = [self.hw, self.ts/2, self.ts/2, self.hl]
            t = [self.ts, self.ts, self.ts]
        return ThinWalledSection(y, z, t)
    def __repr__(self):
        if self.label is None:
            outstr = '<L-Section>'
        else:
            outstr = f'<L-Section {self.label:s}>'
        return outstr
    def __str__(self):
        mdstr = self.section_heading('L-Section')
        table = MDTable()
        table.add_column(f'h<sub>w</sub> ({config.lunit:s})', config.l1frm, data=[self.hw])
        table.add_column(f'w<sub>f</sub> ({config.lunit:s})', config.l1frm, data=[self.wf])
        table.add_column(f't<sub>s</sub> ({config.lunit:s})', config.l1frm, data=[self.ts])
        table.add_column(f'r<sub>m</sub> ({config.lunit:s})', config.l1frm, data=[self.rm])
        if self.hl != 0.0:
            table.add_column('h<sub>l</sub>', config.l1frm, data=[self.hl])
        mdstr += str(table)
        mdstr += self.section_properties()
        return mdstr
    def _repr_markdown_(self):
        return self.__str__()
