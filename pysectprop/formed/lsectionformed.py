from py2md.classes import MDTable

from .. import config
from ..general.generalsection import GeneralSection
from ..general.thinwalledsection import ThinWalledSection


class LSectionFormed(GeneralSection):
    hw: float = None # Height of web
    wf: float = None # Width of flange
    ts: float = None # Thickness of section
    rm: float = None # Bend radius

    def __init__(self, hw: float, wf: float, ts: float, rm: float,
                 label: str=None) -> None:
        self.hw = hw
        self.wf = wf
        self.ts = ts
        self.rm = rm
        y = [0.0, self.wf, self.wf, self.ts, self.ts, 0.0]
        z = [0.0, 0.0, self.ts, self.ts, self.hw, self.hw]
        r = [self.rm+self.ts/2, 0.0, 0.0, self.rm-self.ts/2, 0.0, 0.0]
        super().__init__(y, z, r, label=label)

    def to_thin_walled_section(self) -> ThinWalledSection:
        y = [self.ts/2, self.ts/2, self.wf]
        z = [self.hw, self.ts/2, self.ts/2]
        t = [self.ts, self.ts]
        return ThinWalledSection(y, z, t)

    def _repr_markdown_(self) -> str:
        mdstr = self.section_heading('L-Section')
        table = MDTable()
        table.add_column(f'h<sub>w</sub> ({config.lunit:s})',
                         config.l1frm, data=[self.hw])
        table.add_column(f'w<sub>f</sub> ({config.lunit:s})',
                         config.l1frm, data=[self.wf])
        table.add_column(f't<sub>s</sub> ({config.lunit:s})',
                         config.l1frm, data=[self.ts])
        table.add_column(f'r<sub>m</sub> ({config.lunit:s})',
                         config.l1frm, data=[self.rm])
        mdstr += table._repr_markdown_()
        mdstr += self.section_properties(outtype='md')
        return mdstr

    def __str__(self) -> str:
        outstr = self.section_heading('L-Section')
        table = MDTable()
        table.add_column(f'h_w ({config.lunit:s})',
                         config.l1frm, data=[self.hw])
        table.add_column(f'w_f ({config.lunit:s})',
                         config.l1frm, data=[self.wf])
        table.add_column(f't_s ({config.lunit:s})',
                         config.l1frm, data=[self.ts])
        table.add_column(f'r_m ({config.lunit:s})',
                         config.l1frm, data=[self.rm])
        outstr += table.__str__()
        outstr += self.section_properties(outtype=str)
        return outstr

    def __repr__(self) -> str:
        if self.label is None:
            outstr = '<L-Section>'
        else:
            outstr = f'<L-Section {self.label:s}>'
        return outstr
