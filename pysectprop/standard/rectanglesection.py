from py2md.classes import MDTable

from .. import config
from ..general.generalsection import GeneralSection


class RectangleSection(GeneralSection):
    h: float = None
    b: float = None
    rc: float = None

    def __init__(self, h: float, b: float, rc: float=0.0, label: str=None) -> None:
        self.h = h
        self.b = b
        self.rc = rc
        y = [self.b/2,
             self.b/2, -self.b/2,
             -self.b/2]
        z = [-self.h/2,
             self.h/2, self.h/2, -self.h/2]
        r = [self.rc, self.rc, self.rc, self.rc]
        super().__init__(y, z, r, label=label)

    def _repr_markdown_(self) -> str:
        mdstr = self.section_heading('Rectangle-Section')
        table = MDTable()
        table.add_column(f'h ({config.lunit:s})',
                         config.l1frm, data=[self.h])
        table.add_column(f'b ({config.lunit:s})',
                         config.l1frm, data=[self.b])
        mdstr += table._repr_markdown_()
        mdstr += self.section_properties(outtype='md')
        return mdstr

    def __str__(self) -> str:
        outstr = self.section_heading('Rectangle-Section')
        table = MDTable()
        table.add_column(f'h ({config.lunit:s})',
                         config.l1frm, data=[self.h])
        table.add_column(f'b ({config.lunit:s})',
                         config.l1frm, data=[self.b])
        outstr += table.__str__()
        outstr += self.section_properties(outtype=str)
        return outstr

    def __repr__(self) -> str:
        if self.label is None:
            outstr = '<Rectangle-Section>'
        else:
            outstr = f'<Rectangle-Section {self.label:s}>'
        return outstr
