from py2md.classes import MDTable
from ..general.generalsection import GeneralSection
from .. import config

class CircleSection(GeneralSection):
    d = None
    def __init__(self, d: float, label: str=None):
        self.d = d
        radius = self.d/2
        y = [radius, -radius, -radius, radius]
        z = [radius, radius, -radius, -radius]
        r = [radius, radius, radius, radius]
        super().__init__(y, z, r, label=label)
    def __repr__(self):
        if self.label is None:
            outstr = '<Circle-Section>'
        else:
            outstr = f'<Circle-Section {self.label:s}>'
        return outstr
    def __str__(self):
        mdstr = self.section_heading('Circle-Section')
        table = MDTable()
        table.add_column(f'Diameter ({config.lunit:s})', config.l1frm, data=[self.d])
        mdstr += str(table)
        mdstr += self.section_properties()
        return mdstr
    def _repr_markdown_(self):
        return self.__str__()
