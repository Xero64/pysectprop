from py2md.classes import MDTable

from .. import config
from ..general.generalsection import GeneralSection


class TSection(GeneralSection):
    hw: float = None
    tw: float = None
    wf: float = None
    tf: float = None
    rf: float = None

    def __init__(self, hw: float, tw: float, wf: float, tf: float,
                 rf: float=0.0, label: str=None):
        self.hw = hw
        self.tw = tw
        self.wf = wf
        self.tf = tf
        self.rf = rf
        y = [-self.wf/2, -self.wf/2, -self.tw/2, -self.tw/2,
             self.tw/2, self.tw/2, self.wf/2, self.wf/2]
        z = [self.hw, self.hw-self.tf, self.hw-self.tf, 0.0,
             0.0, self.hw-self.tf, self.hw-self.tf, self.hw]
        r = [0.0, 0.0, self.rf, 0.0, 0.0, self.rf, 0.0, 0.0]
        super().__init__(y, z, r, label=label)

    def _repr_markdown_(self) -> str:
        mdstr = self.section_heading('T-Section')
        table = MDTable()
        table.add_column(f'h<sub>w</sub> ({config.lunit:s})', config.l1frm,
                         data=[self.hw])
        table.add_column(f't<sub>w</sub> ({config.lunit:s})', config.l1frm,
                         data=[self.tw])
        table.add_column(f'w<sub>f</sub> ({config.lunit:s})', config.l1frm,
                         data=[self.wf])
        table.add_column(f't<sub>f</sub> ({config.lunit:s})', config.l1frm,
                         data=[self.tf])
        table.add_column(f'r<sub>f</sub> ({config.lunit:s})', config.l1frm,
                         data=[self.rf])
        mdstr += table._repr_markdown_()
        mdstr += self.section_properties(outtype='md')
        return mdstr

    def __str__(self) -> str:
        mdstr = self.section_heading('T-Section')
        table = MDTable()
        table.add_column(f'h_w ({config.lunit:s})', config.l1frm, data=[self.hw])
        table.add_column(f't_w ({config.lunit:s})', config.l1frm, data=[self.tw])
        table.add_column(f'w_f ({config.lunit:s})', config.l1frm, data=[self.wf])
        table.add_column(f't_f ({config.lunit:s})', config.l1frm, data=[self.tf])
        table.add_column(f'r_f ({config.lunit:s})', config.l1frm, data=[self.rf])
        mdstr += table.__str__()
        mdstr += self.section_properties(outtype=str)
        return mdstr

    def __repr__(self) -> str:
        if self.label is None:
            outstr = '<T-Section>'
        else:
            outstr = f'<T-Section {self.label:s}>'
        return outstr
