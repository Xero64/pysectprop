from py2md.classes import MDTable

from .. import config
from ..general.generalsection import GeneralSection


class JSection(GeneralSection):
    hw: float = None
    tw: float = None
    wuf: float = None
    wlf: float = None
    tuf: float = None
    tlf: float = None
    ruf: float = None
    rlf: float = None

    def __init__(self, hw: float, tw: float, wuf: float, tuf: float,
                 wlf: float, tlf: float, rlf: float=0.0, ruf: float=0.0,
                 label: str=None) -> None:
        self.hw = hw
        self.tw = tw
        self.wuf = wuf
        self.tuf = tuf
        self.wlf = wlf
        self.tlf = tlf
        self.rlf = rlf
        self.ruf = ruf
        y = [self.tw/2, self.tw/2, self.wuf/2, self.wuf/2,
             -self.wuf/2, -self.wuf/2, -self.tw/2, -self.tw/2,
             -self.wlf, -self.wlf]
        z = [0.0, self.hw-self.tuf, self.hw-self.tuf, self.hw,
             self.hw, self.hw-self.tuf, self.hw-self.tuf,
             self.tlf, self.tlf, 0.0]
        r = [0.0, self.ruf, 0.0, 0.0, 0.0, 0.0, self.ruf,
             self.rlf, 0.0, 0.0]
        super().__init__(y, z, r, label=label)

    def _repr_markdown_(self) -> str:
        mdstr = self.section_heading('J-Section')
        table = MDTable()
        table.add_column(f'h<sub>w</sub> ({config.lunit:s})', config.l1frm,
                         data=[self.hw])
        table.add_column(f't<sub>w</sub> ({config.lunit:s})', config.l1frm,
                         data=[self.tw])
        table.add_column(f'w<sub>uf</sub> ({config.lunit:s})', config.l1frm,
                         data=[self.wuf])
        table.add_column(f't<sub>uf</sub> ({config.lunit:s})', config.l1frm,
                         data=[self.tuf])
        table.add_column(f'w<sub>lf</sub> ({config.lunit:s})', config.l1frm,
                         data=[self.wlf])
        table.add_column(f't<sub>lf</sub> ({config.lunit:s})', config.l1frm,
                         data=[self.tlf])
        table.add_column(f'r<sub>lf</sub> ({config.lunit:s})', config.l1frm,
                         data=[self.rlf])
        table.add_column(f'r<sub>uf</sub> ({config.lunit:s})', config.l1frm,
                         data=[self.ruf])
        mdstr += table._repr_markdown_()
        mdstr += self.section_properties(outtype='md')
        return mdstr

    def __str__(self) -> str:
        outstr = self.section_heading('J-Section')
        table = MDTable()
        table.add_column(f'h_w ({config.lunit:s})', config.l1frm, data=[self.hw])
        table.add_column(f't_w ({config.lunit:s})', config.l1frm, data=[self.tw])
        table.add_column(f'w_uf ({config.lunit:s})', config.l1frm, data=[self.wuf])
        table.add_column(f't_uf ({config.lunit:s})', config.l1frm, data=[self.tuf])
        table.add_column(f'w_lf ({config.lunit:s})', config.l1frm, data=[self.wlf])
        table.add_column(f't_lf ({config.lunit:s})', config.l1frm, data=[self.tlf])
        table.add_column(f'r_lf ({config.lunit:s})', config.l1frm, data=[self.rlf])
        table.add_column(f'r_uf ({config.lunit:s})', config.l1frm, data=[self.ruf])
        outstr += table.__str__()
        outstr += self.section_properties(outtype=str)
        return outstr

    def __repr__(self) -> str:
        if self.label is None:
            outstr = '<J-Section>'
        else:
            outstr = f'<J-Section {self.label:s}>'
        return outstr
