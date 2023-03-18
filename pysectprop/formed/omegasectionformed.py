from py2md.classes import MDTable
from ..general.generalsection import GeneralSection
from ..general.thinwalledsection import ThinWalledSection
from .. import config

class OmegaSectionFormed(GeneralSection):
    hw: float = None # Height of web
    wuf: float = None # Width of lower flange
    wlf: float = None # Width of upper flange
    ts: float = None # Thickness of section
    rm: float = None # Bend radius
    def __init__(self, hw: float, wlf: float, wuf: float, ts: float,
                 rm: float, label: str=None) -> None:
        self.hw = hw
        self.wlf = wlf
        self.wuf = wuf
        self.ts = ts
        self.rm = rm
        y = [-self.wlf-self.wuf/2+self.ts, -self.wuf/2+self.ts,
             -self.wuf/2+self.ts, self.wuf/2-self.ts, self.wuf/2-self.ts,
             self.wlf+self.wuf/2-self.ts, self.wlf+self.wuf/2-self.ts,
             self.wuf/2, self.wuf/2, -self.wuf/2, -self.wuf/2,
             -self.wlf-self.wuf/2+self.ts]
        z = [0.0, 0.0, self.hw-self.ts, self.hw-self.ts, 0.0, 0.0,
             self.ts, self.ts, self.hw, self.hw, self.ts, self.ts]
        r = [0.0, self.rm+self.ts/2, self.rm-self.ts/2, self.rm-self.ts/2,
             self.rm+self.ts/2, 0.0, 0.0, self.rm-self.ts/2, self.rm+self.ts/2,
             self.rm+self.ts/2, self.rm-self.ts/2, 0.0]
        super().__init__(y, z, r, label=label)
    def to_thin_walled_section(self) -> ThinWalledSection:
        y = [-self.wlf-self.wuf/2+self.ts, -self.wuf/2+self.ts/2, -self.wuf/2+self.ts/2,
             self.wuf/2-self.ts/2, self.wuf/2-self.ts/2, self.wlf+self.wuf/2-self.ts]
        z = [self.ts/2, self.ts/2, self.hw-self.ts/2, self.hw-self.ts/2,
             self.ts/2, self.ts/2]
        t = [self.ts, self.ts, self.ts, self.ts, self.ts]
        return ThinWalledSection(y, z, t)
    def _repr_markdown_(self) -> str:
        mdstr = self.section_heading('Omega-Section Formed')
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
        outstr = self.section_heading('Omega-Section Formed')
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
        outstr += str(table)
        outstr += self.section_properties(outtype='str')
        return outstr
    def __repr__(self) -> str:
        if self.label is None:
            outstr = '<Omega-Section Formed>'
        else:
            outstr = f'<Omega-Section Formed: {self.label:s}>'
        return outstr
