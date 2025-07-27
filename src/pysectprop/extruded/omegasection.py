from py2md.classes import MDTable

from .. import config
from ..general.generalsection import GeneralSection


class OmegaSection(GeneralSection):
    hw: float = None # Height of web
    tw: float = None # Thickness of web
    wuf: float = None # Width of upper flange
    tuf: float = None # Thickness of upper flange
    wlf: float = None # Width of lower flange
    tlf: float = None # Thickness of lower flange
    ruf: float = None # Radius of upper flange
    rlf: float = None # Radius of lower flange

    def __init__(self, hw: float, tw: float, wuf: float, tuf: float,
                 wlf: float, tlf: float, ruf: float=0.0, rlf: float=0.0,
                 label: str=None) -> None:
        self.hw = hw
        self.tw = tw
        self.wuf = wuf
        self.tuf = tuf
        self.wlf = wlf
        self.tlf = tlf
        self.ruf = ruf
        self.rlf = rlf
        y = [0.0, self.wuf/2, self.wuf/2,
             self.wuf/2-self.tw+self.wlf, self.wuf/2-self.tw+self.wlf,
             self.wuf/2-self.tw, self.wuf/2-self.tw, 0.0, self.tw-self.wuf/2,
             self.tw-self.wuf/2, self.tw-self.wuf/2-self.wlf,
             self.tw-self.wuf/2-self.wlf, -self.wuf/2, -self.wuf/2]
        z = [0.0, 0.0, self.hw-self.tlf, self.hw-self.tlf, self.hw, self.hw,
             self.tuf, self.tuf, self.tuf, self.hw, self.hw, self.hw-self.tlf,
             self.hw-self.tlf, 0.0]
        r = [0.0, 0.0, self.rlf, 0.0, 0.0, 0.0, self.ruf, 0.0,
             self.ruf, 0.0, 0.0, 0.0, self.rlf, 0.0]
        super().__init__(y, z, r, label=label)

    def _repr_markdown_(self) -> str:
        mdstr = self.section_heading('Omega-Section')
        table = MDTable()
        table.add_column(f'h<sub>w</sub> ({config.lunit:s})',
                         config.l1frm, data=[self.hw])
        table.add_column(f't<sub>w</sub> ({config.lunit:s})',
                         config.l1frm, data=[self.tw])
        table.add_column(f'w<sub>uf</sub> ({config.lunit:s})',
                         config.l1frm, data=[self.wuf])
        table.add_column(f't<sub>uf</sub> ({config.lunit:s})',
                         config.l1frm, data=[self.tuf])
        table.add_column(f'w<sub>lf</sub> ({config.lunit:s})',
                         config.l1frm, data=[self.wlf])
        table.add_column(f't<sub>lf</sub> ({config.lunit:s})',
                         config.l1frm, data=[self.tlf])
        table.add_column(f'r<sub>uf</sub> ({config.lunit:s})',
                         config.l1frm, data=[self.ruf])
        table.add_column(f'r<sub>lf</sub> ({config.lunit:s})',
                         config.l1frm, data=[self.rlf])
        mdstr += table._repr_markdown_()
        mdstr += self.section_properties(outtype='md')
        return mdstr

    def __str__(self) -> str:
        outstr = self.section_heading('Omega-Section')
        table = MDTable()
        table.add_column(f'h_w ({config.lunit:s})',
                         config.l1frm, data=[self.hw])
        table.add_column(f't_w ({config.lunit:s})',
                         config.l1frm, data=[self.tw])
        table.add_column(f'w_uf ({config.lunit:s})',
                         config.l1frm, data=[self.wuf])
        table.add_column(f't_uf ({config.lunit:s})',
                         config.l1frm, data=[self.tuf])
        table.add_column(f'w_lf ({config.lunit:s})',
                         config.l1frm, data=[self.wlf])
        table.add_column(f't_lf ({config.lunit:s})',
                         config.l1frm, data=[self.tlf])
        table.add_column(f'r_uf ({config.lunit:s})',
                         config.l1frm, data=[self.ruf])
        table.add_column(f'r_lf ({config.lunit:s})',
                         config.l1frm, data=[self.rlf])
        outstr += table.__str__()
        outstr += self.section_properties(outtype=str)
        return outstr

    def __repr__(self) -> str:
        if self.label is None:
            outstr = '<Omega-Section>'
        else:
            outstr = f'<Omega-Section {self.label:s}>'
        return outstr
