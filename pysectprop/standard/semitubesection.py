from py2md.classes import MDTable

from .. import config
from ..general.generalsection import GeneralSection


class SemiTubeSection(GeneralSection):
    do: float = None
    di: float = None

    def __init__(self, do: float, di: float, label: str=None):
        self.do = do
        self.di = di
        ro = self.do/2
        ri = self.di/2
        y = [ro, ro, -ro, -ro, -ri, -ri, ri, ri]
        z = [0.0, ro, ro, 0.0, 0.0, ri, ri, 0.0]
        r = [0.0, ro, ro, 0.0, 0.0, ri, ri, 0.0]
        super().__init__(y, z, r, label=label)

    def _repr_markdown_(self) -> str:
        mdstr = self.section_heading('Semi-Tube-Section')
        table = MDTable()
        table.add_column(f'd<sub>o</sub> ({config.lunit:s})',
                         config.l1frm, data=[self.do])
        table.add_column(f'd<sub>i</sub> ({config.lunit:s})',
                         config.l1frm, data=[self.di])
        mdstr += table._repr_markdown_()
        mdstr += self.section_properties(outtype='md')
        return mdstr

    def __str__(self) -> str:
        outstr = self.section_heading('Semi-Tube-Section')
        table = MDTable()
        table.add_column(f'd_o ({config.lunit:s})',
                         config.l1frm, data=[self.do])
        table.add_column(f'd_i ({config.lunit:s})',
                         config.l1frm, data=[self.di])
        outstr += table.__str__()
        outstr += self.section_properties(outtype=str)
        return outstr

    def __repr__(self):
        if self.label is None:
            outstr = '<Semi-Tube-Section>'
        else:
            outstr = f'<Semi-Tube-Section {self.label:s}>'
        return outstr
