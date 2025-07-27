from py2md.classes import MDTable

from .. import config
from ..general.hollowsection import HollowSection
from ..standard.circlesection import CircleSection


class TubeSection(HollowSection):
    do: float = None
    di: float = None

    def __init__(self, do: float, di: float, label: str=None) -> None:
        self.do = do
        self.di = di
        outer = CircleSection(do)
        inner = CircleSection(di)
        super().__init__(outer, inner, label=label)

    def _repr_markdown_(self) -> str:
        mdstr = self.section_heading('Tube-Section')
        table = MDTable()
        table.add_column(f'd<sub>o</sub> ({config.lunit:s})',
                         config.l1frm, data=[self.do])
        table.add_column(f'd<sub>i</sub> ({config.lunit:s})',
                         config.l1frm, data=[self.di])
        mdstr += table._repr_markdown_()
        mdstr += self.section_properties(outtype='md')
        return mdstr

    def __str__(self) -> str:
        outstr = self.section_heading('Tube-Section')
        table = MDTable()
        table.add_column(f'd_o ({config.lunit:s})',
                         config.l1frm, data=[self.do])
        table.add_column(f'd_i ({config.lunit:s})',
                         config.l1frm, data=[self.di])
        outstr += table.__str__()
        outstr += self.section_properties(outtype=str)
        return outstr

    def __repr__(self) -> str:
        if self.label is None:
            outstr = '<Tube-Section>'
        else:
            outstr = f'<Tube-Section {self.label:s}>'
        return outstr
