from py2md.classes import MDHeading, MDTable

from .. import config


class Material():
    E: float = None
    Ec: float = None
    Ftu: float = None
    Fcu: float = None
    Fty: float = None
    Fcy: float = None
    label: str = None

    def __init__(self, E: float, Ec: float=None, label: str=None) -> None:
        self.E = E
        self.Ec = Ec
        if self.Ec is None:
            self.Ec = self.E
        self.label = label

    def set_yield_strengths(self, Fty: float, Fcy: float) -> None:
        self.Fty = Fty
        self.Fcy = Fcy

    def set_ultimate_strengths(self, Ftu: float, Fcu: float | None = None) -> None:
        self.Ftu = Ftu
        if Fcu is None:
            self.Fcu = Ftu
        else:
            self.Fcu = Fcu

    def _repr_markdown_(self) -> str:
        if self.label is None:
            heading  = MDHeading('Material Properties', 3)
        else:
            heading  = MDHeading(f'Material Properties - {self.label:s}', 3)
        mdstr = str(heading)
        table = MDTable()
        table.add_column(f'E ({config.sunit:s})', config.efrm, data=[self.E])
        table.add_column(f'E<sub>c</sub> ({config.sunit:s})',
                         config.efrm, data=[self.Ec])
        if self.Fty is not None:
            table.add_column(f'F<sub>ty</sub> ({config.sunit:s})',
                             config.sfrm, data=[self.Fty])
        if self.Fcy is not None:
            table.add_column(f'F<sub>cy</sub> ({config.sunit:s})',
                             config.sfrm, data=[self.Fcy])
        if self.Ftu is not None:
            table.add_column(f'F<sub>tu</sub> ({config.sunit:s})',
                             config.sfrm, data=[self.Ftu])
        if self.Fcu is not None:
            table.add_column(f'F<sub>cu</sub> ({config.sunit:s})',
                             config.sfrm, data=[self.Fcu])
        mdstr += table._repr_markdown_()
        return mdstr

    def __str__(self) -> str:
        if self.label is None:
            heading  = MDHeading('Material Properties', 3)
        else:
            heading  = MDHeading(f'Material Properties - {self.label:s}', 3)
        outstr = str(heading)
        table = MDTable()
        table.add_column(f'E ({config.sunit:s})', config.efrm, data=[self.E])
        table.add_column(f'Ec ({config.sunit:s})',
                         config.efrm, data=[self.Ec])
        if self.Fty is not None:
            table.add_column(f'Fty ({config.sunit:s})',
                             config.sfrm, data=[self.Fty])
        if self.Fcy is not None:
            table.add_column(f'Fcy ({config.sunit:s})',
                             config.sfrm, data=[self.Fcy])
        if self.Ftu is not None:
            table.add_column(f'Ftu ({config.sunit:s})',
                             config.sfrm, data=[self.Ftu])
        if self.Fcu is not None:
            table.add_column(f'Fcu ({config.sunit:s})',
                             config.sfrm, data=[self.Fcu])
        outstr += table.__str__()
        return outstr

    def __repr__(self) -> str:
        if self.label is None:
            outstr = '<Material>'
        else:
            outstr = f'<Material {self.label:s}>'
        return outstr
