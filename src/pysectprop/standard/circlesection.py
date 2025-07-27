from py2md.classes import MDTable

from .. import config
from ..general.generalsection import GeneralSection


class CircleSection(GeneralSection):
    d: float = None

    def __init__(self, d: float, label: str=None) -> None:
        self.d = d
        radius = self.d/2
        y = [radius, -radius, -radius, radius]
        z = [radius, radius, -radius, -radius]
        r = [radius, radius, radius, radius]
        super().__init__(y, z, r, label=label)

    def _repr_markdown_(self) -> str:
        mdstr = self.section_heading('Circle-Section')
        table = MDTable()
        table.add_column(f'd ({config.lunit:s})',
                         config.l1frm, data=[self.d])
        mdstr += table._repr_markdown_()
        mdstr += self.section_properties(outtype='md')
        return mdstr

    def __str__(self) -> str:
        outstr = self.section_heading('Circle-Section')
        table = MDTable()
        table.add_column(f'd ({config.lunit:s})',
                         config.l1frm, data=[self.d])
        outstr += table.__str__()
        outstr += self.section_properties(outtype=str)
        return outstr

    def __repr__(self) -> str:
        if self.label is None:
            outstr = '<Circle-Section>'
        else:
            outstr = f'<Circle-Section {self.label:s}>'
        return outstr
