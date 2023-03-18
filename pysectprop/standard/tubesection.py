from py2md.classes import MDTable
from ..general.generalsection import GeneralSection
from .. import config

class TubeSection(GeneralSection):
    do = None
    di = None
    def __init__(self, do: float, di: float, label: str=None):
        self.do = do
        self.di = di
        ro = self.do/2
        ri = self.di/2
        y = [ro, ro, -ro, -ro, ro, ro, ri, ri, -ri, -ri, ri, ri]
        z = [0.0, ro, ro, -ro, -ro, 0.0, 0.0, -ri, -ri, ri, ri, 0.0]
        r = [0.0, ro, ro, ro, ro, 0.0, 0.0, ri, ri, ri, ri, 0.0]
        super().__init__(y, z, r, label=label)
    def __repr__(self):
        if self.label is None:
            outstr = '<TubeSection>'
        else:
            outstr = f'<TubeSection {self.label:s}>'
        return outstr
    def __str__(self):
        mdstr = self.section_heading('Tube Section')
        table = MDTable()
        table.add_column(f'd<sub>o</sub> ({config.lunit:s})',
                         config.l1frm, data=[self.do])
        table.add_column(f'd<sub>i</sub> ({config.lunit:s})',
                         config.l1frm, data=[self.di])
        mdstr += str(table)
        mdstr += self.section_properties()
        return mdstr
    def _repr_markdown_(self):
        return self.__str__()
