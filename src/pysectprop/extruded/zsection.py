from py2md.classes import MDTable

from .. import config
from ..general.generalsection import GeneralSection
from ..general.thinwalledsection import ThinWalledSection


class ZSection(GeneralSection):
    hw: float = None
    tw: float = None
    wlf: float = None
    tlf: float = None
    wuf: float = None
    tuf: float = None
    rlf: float = None
    ruf: float = None

    def __init__(self, hw: float, tw: float, wlf: float, tlf: float,
                 wuf: float, tuf: float, ruf: float=0.0, rlf: float=0.0,
                 label: str=None) -> None:
        self.hw = hw
        self.tw = tw
        self.wlf = wlf
        self.tlf = tlf
        self.wuf = wuf
        self.tuf = tuf
        self.ruf = ruf
        self.rlf = rlf
        y = [0.0, self.wlf, self.wlf, self.tw, self.tw,
             self.tw-self.wuf, self.tw-self.wuf, 0.0]
        z = [0.0, 0.0, self.tlf, self.tlf, self.hw,
             self.hw, self.hw - self.tuf, self.hw - self.tuf]
        r = [0.0, 0.0, 0.0, self.ruf, 0.0, 0.0, 0.0, self.rlf]
        super().__init__(y, z, r, label=label)

    def to_thin_walled_section(self) -> ThinWalledSection:
        y = [self.wlf, self.tw/2, self.tw/2, self.tw/2-self.wuf]
        z = [self.tlf/2, self.tlf/2, self.hw-self.tuf/2, self.hw-self.tuf/2]
        t = [self.tlf, self.tw, self.tuf]
        return ThinWalledSection(y, z, t, label=self.label)

    def _repr_markdown_(self) -> str:
        mdstr = self.section_heading('Z-Section')
        table = MDTable()
        table.add_column(f'h<sub>w</sub> ({config.lunit:s})', config.l1frm,
                         data=[self.hw])
        table.add_column(f't<sub>w</sub> ({config.lunit:s})', config.l1frm,
                         data=[self.tw])
        table.add_column(f'w<sub>lf</sub> ({config.lunit:s})', config.l1frm,
                         data=[self.wlf])
        table.add_column(f't<sub>lf</sub> ({config.lunit:s})', config.l1frm,
                         data=[self.tlf])
        table.add_column(f'w<sub>uf</sub> ({config.lunit:s})', config.l1frm,
                         data=[self.wuf])
        table.add_column(f't<sub>uf</sub> ({config.lunit:s})', config.l1frm,
                         data=[self.tuf])
        table.add_column(f'r<sub>uf</sub> ({config.lunit:s})', config.l1frm,
                         data=[self.ruf])
        table.add_column(f'r<sub>lf</sub> ({config.lunit:s})', config.l1frm,
                         data=[self.rlf])
        mdstr += table._repr_markdown_()
        mdstr += self.section_properties(outtype='md')
        return mdstr

    def __str__(self) -> str:
        outstr = self.section_heading('Z-Section')
        table = MDTable()
        table.add_column(f'h_w ({config.lunit:s})', config.l1frm, data=[self.hw])
        table.add_column(f't_w ({config.lunit:s})', config.l1frm, data=[self.tw])
        table.add_column(f'w_uf ({config.lunit:s})', config.l1frm, data=[self.wlf])
        table.add_column(f't_uf ({config.lunit:s})', config.l1frm, data=[self.tlf])
        table.add_column(f'w_lf ({config.lunit:s})', config.l1frm, data=[self.wuf])
        table.add_column(f't_lf ({config.lunit:s})', config.l1frm, data=[self.tuf])
        table.add_column(f'r_uf ({config.lunit:s})', config.l1frm, data=[self.ruf])
        table.add_column(f'r_lf ({config.lunit:s})', config.l1frm, data=[self.rlf])
        outstr += table.__str__()
        outstr += self.section_properties(outtype=str)
        return outstr

    def __repr__(self) -> str:
        if self.label is None:
            outstr = '<Z-Section>'
        else:
            outstr = f'<Z-Section {self.label:s}>'
        return outstr
