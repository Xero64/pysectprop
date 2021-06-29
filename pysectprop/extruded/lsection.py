from py2md.classes import MDTable
from ..general.generalsection import GeneralSection
from .. import config

class LSection(GeneralSection):
    hw = None
    tw = None
    wf = None
    tf = None
    rc = None
    def __init__(self, hw: float, tw: float, wf: float, tf: float, rc: float=0.0, label: str=None):
        self.hw = hw
        self.tw = tw
        self.wf = wf
        self.tf = tf
        self.rc = rc
        y = [0.0, self.wf, self.wf, self.tw, self.tw, 0.0]
        z = [0.0, 0.0, self.tf, self.tf, self.hw, self.hw]
        r = [0.0, 0.0, 0.0, self.rc, 0.0, 0.0]
        super().__init__(y, z, r, label=label)
    def __repr__(self):
        if self.label is None:
            outstr = '<L-Section>'
        else:
            outstr = f'<L-Section {self.label:s}>'
        return outstr
    def __str__(self):
        mdstr = self.section_heading('L-Section')
        table = MDTable()
        table.add_column(f'h<sub>w</sub> ({config.lunit:s})', config.l1frm, data=[self.hw])
        table.add_column(f't<sub>w</sub> ({config.lunit:s})', config.l1frm, data=[self.tw])
        table.add_column(f'w<sub>f</sub> ({config.lunit:s})', config.l1frm, data=[self.wf])
        table.add_column(f't<sub>f</sub> ({config.lunit:s})', config.l1frm, data=[self.tf])
        table.add_column(f'r<sub>c</sub> ({config.lunit:s})', config.l1frm, data=[self.rc])
        mdstr += str(table)
        mdstr += self.section_properties()
        return mdstr
    def _repr_markdown_(self):
        return self.__str__()
