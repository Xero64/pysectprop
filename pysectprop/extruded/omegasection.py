from py2md.classes import MDTable
from ..general.generalsection import GeneralSection
from .. import config

class OmegaSection(GeneralSection):
    hw = None
    tw = None
    wf = None
    tf = None
    wl = None
    tl = None
    rf = None
    rl = None
    def __init__(self, hw: float, tw: float, wf: float, tf: float,
                 wl: float, tl: float, rf: float=0.0, rl: float=0.0, label: str=None):
        self.hw = hw
        self.tw = tw
        self.wf = wf
        self.tf = tf
        self.wl = wl
        self.tl = tl
        self.rf = rf
        self.rl = rl
        y = [0.0, self.wf/2, self.wf/2,
             self.wf/2-self.tw+self.wl, self.wf/2-self.tw+self.wl,
             self.wf/2-self.tw, self.wf/2-self.tw, 0.0, self.tw-self.wf/2, self.tw-self.wf/2,
             self.tw-self.wf/2-self.wl, self.tw-self.wf/2-self.wl,
             -self.wf/2, -self.wf/2, 0.0]
        z = [0.0, 0.0, self.hw-self.tl, self.hw-self.tl, self.hw, self.hw,
             self.tf, self.tf, self.tf, self.hw, self.hw, self.hw-self.tl,
             self.hw-self.tl, 0.0, 0.0]
        r = [0.0, 0.0, self.rl, 0.0, 0.0, 0.0, self.rf, 0.0,
             self.rf, 0.0, 0.0, 0.0, self.rl, 0.0, 0.0]
        super().__init__(y, z, r, label=label)
    def __repr__(self):
        if self.label is None:
            outstr = '<Omega-Section>'
        else:
            outstr = f'<Omega-Section {self.label:s}>'
        return outstr
    def __str__(self):
        mdstr = self.section_heading('Omega-Section')
        table = MDTable()
        table.add_column(f'h<sub>w</sub> ({config.lunit:s})', config.l1frm, data=[self.hw])
        table.add_column(f't<sub>w</sub> ({config.lunit:s})', config.l1frm, data=[self.tw])
        table.add_column(f'w<sub>f</sub> ({config.lunit:s})', config.l1frm, data=[self.wf])
        table.add_column(f't<sub>f</sub> ({config.lunit:s})', config.l1frm, data=[self.tf])
        table.add_column(f'w<sub>l</sub> ({config.lunit:s})', config.l1frm, data=[self.wl])
        table.add_column(f't<sub>l</sub> ({config.lunit:s})', config.l1frm, data=[self.tl])
        table.add_column(f'r<sub>f</sub> ({config.lunit:s})', config.l1frm, data=[self.rf])
        table.add_column(f'r<sub>l</sub> ({config.lunit:s})', config.l1frm, data=[self.rl])
        mdstr += str(table)
        mdstr += self.section_properties()
        return mdstr
    def _repr_markdown_(self):
        return self.__str__()
