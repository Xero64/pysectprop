from py2md.classes import MDTable
from ..general.generalsection import GeneralSection
from .. import config

# S-Section Profile with upper and lower lip profile can be created (Angled flanges to be Added)

class SSection(GeneralSection):
    hw = None
    tw = None
    wf1 = None
    tf1 = None
    wf2 = None
    tf2 = None
    tl1 = None # Lip thickness
    hl1 = None # Lip height
    tl2 = None
    hl2 = None
    def __init__(self, hw: float, tw: float, wf1: float, tf1: float, wf2: float, tf2: float,
                 tl1: float=0.0, hl1: float=0.0, tl2: float=0.0, hl2: float=0.0, label: str=None):
        self.hw = hw
        self.tw = tw
        self.wf1 = wf1
        self.tf1 = tf1
        self.wf2 = wf2
        self.tf2 = tf2
        self.tl1 = tl1
        self.hl1 = hl1
        self.tl2 = tl2
        self.hl2 = hl2
        if tl1 != 0.0 and tl2 != 0.0: # Double Lip
            y = [0.0, self.wf1, self.wf1, self.wf1 - self.tl1, self.wf1 - self.tl1, self.tw,
                 self.tw, self.tw-self.wf2, self.tw-self.wf2, self.tw-self.wf2+self.tl2,
                 self.tw-self.wf2+self.tl2, 0.0]
            z = [0.0, 0.0, self.hl1, self.hl1, self.tf1, self.tf1,
                 self.hw, self.hw, self.hw-self.hl2, self.hw-self.hl2,
                 self.hw-self.tf2, self.hw-self.tf2]
            r = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        elif tl1 != 0.0: # Single Lip
            y = [0.0, self.wf1, self.wf1, self.wf1 - self.tl1, self.wf1-self.tl1,
                 self.tw, self.tw, self.tw-self.wf2, self.tw-self.wf2, 0.0]
            z = [0.0, 0.0, self.hl1, self.hl1, self.tf1, self.tf1,self.hw, self.hw,
                 self.hw-self.tf2, self.hw-self.tf2, self.hw-self.tf2]
            r = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        super().__init__(y, z, r, label=label)
    def __repr__(self):
        if self.label is None:
            outstr = '<S-Section>'
        else:
            outstr = f'<S-Section {self.label:s}>'
        return outstr
    def __str__(self):
        mdstr = self.section_heading('S-Section')
        table = MDTable()
        table.add_column(f'h<sub>w</sub> ({config.lunit:s})', config.l1frm, data=[self.hw])
        table.add_column(f't<sub>w</sub> ({config.lunit:s})', config.l1frm, data=[self.tw])
        table.add_column(f'w<sub>f1</sub> ({config.lunit:s})', config.l1frm, data=[self.wf1])
        table.add_column(f't<sub>f1</sub> ({config.lunit:s})', config.l1frm, data=[self.tf1])
        table.add_column(f'w<sub>f2</sub> ({config.lunit:s})', config.l1frm, data=[self.wf2])
        table.add_column(f't<sub>f2</sub> ({config.lunit:s})', config.l1frm, data=[self.tf2])
        mdstr += str(table)
        mdstr += self.section_properties()
        return mdstr
    def _repr_markdown_(self):
        return self.__str__()
