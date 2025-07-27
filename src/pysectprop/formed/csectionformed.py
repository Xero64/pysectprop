from py2md.classes import MDTable

from .. import config
from ..general.generalsection import GeneralSection
from ..general.thinwalledsection import ThinWalledSection


class CSectionFormed(GeneralSection):
    hw: float = None # Height of web
    wuf: float = None # Width of lower flange
    wlf: float = None # Width of upper flange
    ts: float = None # Thickness of section
    rm: float = None # Bend radius

    def __init__(self, hw: float, wuf: float, wlf: float, ts: float,
                 rm: float, label: str=None) -> None:
        self.hw = hw
        self.wuf = wuf
        self.wlf = wlf
        self.ts = ts
        self.rm = rm
        y = [0.0, self.wlf, self.wlf, self.ts, self.ts, self.wuf,
             self.wuf, 0.0]
        z = [0.0, 0.0, self.ts, self.ts, self.hw-self.ts,
             self.hw-self.ts, self.hw, self.hw]
        if self.rm < self.ts/2:
            r = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        else:
            ri = self.rm-self.ts/2
            ro = self.rm+self.ts/2
            r = [ro, 0.0, 0.0, ri, ri, 0.0, 0.0, ro]
        super().__init__(y, z, r, label=label)

    def to_thin_walled_section(self) -> ThinWalledSection:
        y = [self.wlf, self.ts/2, self.ts/2, self.wuf]
        z = [self.ts/2, self.ts/2, self.hw-self.ts/2, self.hw-self.ts/2]
        t = [self.ts, self.ts, self.ts]
        return ThinWalledSection(y, z, t)

    def _repr_markdown_(self) -> str:
        mdstr = self.section_heading('C-Section')
        table = MDTable()
        table.add_column(f'h<sub>w</sub> ({config.lunit:s})',
                         config.l1frm, data=[self.hw])
        table.add_column(f'w<sub>lf</sub> ({config.lunit:s})',
                         config.l1frm, data=[self.wlf])
        table.add_column(f'w<sub>uf</sub> ({config.lunit:s})',
                         config.l1frm, data=[self.wuf])
        table.add_column(f't<sub>s</sub> ({config.lunit:s})',
                         config.l1frm, data=[self.ts])
        table.add_column(f'r<sub>m</sub> ({config.lunit:s})',
                         config.l1frm, data=[self.rm])
        mdstr += table._repr_markdown_()
        mdstr += self.section_properties(outtype='md')
        return mdstr

    def __str__(self) -> str:
        mdstr = self.section_heading('C-Section')
        table = MDTable()
        table.add_column(f'h_w ({config.lunit:s})',
                         config.l1frm, data=[self.hw])
        table.add_column(f'w_lf ({config.lunit:s})',
                         config.l1frm, data=[self.wlf])
        table.add_column(f'w_uf ({config.lunit:s})',
                         config.l1frm, data=[self.wuf])
        table.add_column(f't_s ({config.lunit:s})',
                         config.l1frm, data=[self.ts])
        table.add_column(f'r_m ({config.lunit:s})',
                         config.l1frm, data=[self.rm])
        mdstr += table.__str__()
        mdstr += self.section_properties(outtype=str)
        return mdstr

    def __repr__(self) -> str:
        if self.label is None:
            outstr = '<C-Section Formed>'
        else:
            outstr = f'<C-Section Formed {self.label:s}>'
        return outstr
