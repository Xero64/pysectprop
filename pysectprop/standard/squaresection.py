from py2md.classes import MDTable

from .. import config
from ..general.generalsection import GeneralSection


class SquareSection(GeneralSection):
    s: float = None
    rc: float = None

    def __init__(self, s: float, rc: float=0.0, label: str=None) -> None:
        self.s = s
        self.rc = rc
        half = self.s/2
        y = [half, half, -half, -half]
        z = [-half, half, half, -half]
        r = [self.rc, self.rc, self.rc, self.rc]
        super().__init__(y, z, r, label=label)

    def _repr_markdown_(self) -> str:
        mdstr = self.section_heading('Square-Section')
        table = MDTable()
        table.add_column(f's ({config.lunit:s})',
                         config.l1frm, data=[self.s])
        mdstr += table._repr_markdown_()
        mdstr += self.section_properties(outtype='md')
        return mdstr

    def __str__(self) -> str:
        outstr = self.section_heading('Square-Section')
        table = MDTable()
        table.add_column(f's ({config.lunit:s})',
                         config.l1frm, data=[self.s])
        outstr += table.__str__()
        outstr += self.section_properties(outtype=str)
        return outstr

    def __repr__(self) -> str:
        if self.label is None:
            outstr = '<Square-Section>'
        else:
            outstr = f'<Square-Section {self.label:s}>'
        return outstr
