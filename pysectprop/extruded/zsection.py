from py2md.classes import MDTable
from ..general.generalsection import GeneralSection
from .. import config

class ZSection(GeneralSection):
    hw = None
    tw = None
    wf1 = None
    tf1 = None
    wf2 = None
    tf2 = None
    def __init__(self, hw: float, tw: float, wf1: float, tf1: float, wf2: float, tf2: float, r1: float=0.0, r2: float=0.0, label: str=None):
        self.hw = hw
        self.tw = tw
        self.wf1 = wf1
        self.tf1 = tf1
        self.wf2 = wf2
        self.tf2 = tf2
        self.r1 = r1
        self.r2 = r2
        y = [0.0, self.wf1, self.wf1, self.tw, self.tw, self.tw-self.wf2, self.tw-self.wf2, 0.0]
        z = [0.0, 0.0, self.tf1, self.tf1, self.hw, self.hw, self.hw - self.tf2, self.hw - self.tf2]
        r = [0.0, 0.0, 0.0, self.r1, 0.0, 0.0, 0.0, self.r2]
        super().__init__(y, z, r, label=label)
    def __repr__(self):
        if self.label is None:
            outstr = '<Z-Section>'
        else:
            outstr = f'<Z-Section {self.label:s}>'
        return outstr
    def __str__(self):
        mdstr = self.section_heading('Omega-Section')
        table = MDTable()
        table.add_column(f'h<sub>w</sub> ({config.lunit:s})', config.l1frm, data=[self.hw])
        table.add_column(f't<sub>w</sub> ({config.lunit:s})', config.l1frm, data=[self.tw])
        table.add_column(f'w<sub>f1</sub> ({config.lunit:s})', config.l1frm, data=[self.wf1])
        table.add_column(f't<sub>f1</sub> ({config.lunit:s})', config.l1frm, data=[self.tf1])
        table.add_column(f'w<sub>f2</sub> ({config.lunit:s})', config.l1frm, data=[self.wf2])
        table.add_column(f't<sub>f2</sub> ({config.lunit:s})', config.l1frm, data=[self.tf2])
        table.add_column(f'r<sub>1</sub> ({config.lunit:s})', config.l1frm, data=[self.r1])
        table.add_column(f'r<sub>2</sub> ({config.lunit:s})', config.l1frm, data=[self.r2])
        mdstr += str(table)
        mdstr += self.section_properties()
        return mdstr
    def _repr_markdown_(self):
        return self.__str__()
