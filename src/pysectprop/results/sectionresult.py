from math import floor
from typing import TYPE_CHECKING

from py2md.classes import MDHeading, MDTable

from .. import config

if TYPE_CHECKING:
    from ..general.compositesection import CompositeSection
    from ..general.materialsection import MaterialSection


class SectionResult():
    loadcase: str = None
    limit: bool = None
    msmode: bool = None
    totalsection: 'MaterialSection | CompositeSection' = None
    materialsection: 'MaterialSection' = None
    Fx: float = None
    My: float = None
    Mz: float = None
    y: list[float] = None
    z: list[float] = None
    yna: float = None
    zna: float = None
    eps: list[float] = None
    allowed: list[float] = None
    sigma: list[float] = None
    result: list[float] = None

    def __init__(self, materialsection: 'MaterialSection',
                 totalsection: 'CompositeSection | None' = None) -> None:
        self.materialsection = materialsection
        if totalsection is None:
            self.totalsection = materialsection
        else:
            self.totalsection = totalsection
        self.msmode = False

    def set_load(self, loadcase: str, Fx: float, My: float, Mz: float,
                 limit: bool=False) -> None:
        self.loadcase = loadcase
        self.limit = limit
        self.Fx = Fx
        self.My = My
        self.Mz = Mz
        if limit:
            tensall = self.materialsection.material.Fty
            compall = -self.materialsection.material.Fcy
        else:
            tensall = self.materialsection.material.Ftu
            compall = -self.materialsection.material.Fcu
        Emod = self.materialsection.material.E
        EArea = self.totalsection.EA
        EIyy = self.totalsection.EIyy
        EIzz = self.totalsection.EIzz
        EIyz = self.totalsection.EIyz
        cy = self.totalsection.cy
        cz = self.totalsection.cz
        kd = EIyy*EIzz-EIyz**2
        ky = (Mz*EIyy - My*EIyz)/kd
        kz = (My*EIzz - Mz*EIyz)/kd
        self.y, self.z = [], []
        self.yna, self.zna = [], []
        self.eps = []
        self.allowed = []
        self.sigma = []
        self.result = []
        for point in self.materialsection.section.pnts:
            self.y.append(point.y)
            self.z.append(point.z)
            yna = point.y-cy
            zna = point.z-cz
            self.yna.append(yna)
            self.zna.append(zna)
            eps = Fx/EArea + ky*yna+kz*zna
            self.eps.append(eps)
            sigma = eps*Emod
            self.sigma.append(sigma)
            allowed = tensall
            result = float('inf')
            if sigma < 0.0:
                allowed = compall
                result = allowed/sigma
            elif sigma > 0.0:
                allowed = tensall
                result = allowed/sigma
            self.allowed.append(allowed)
            self.result.append(result)

    def _repr_markdown_(self) -> str:
        lctyp = 'Ultimate'
        if self.limit:
            lctyp = 'Limit'
        msl = self.materialsection.label
        mdstr = ''
        heading = MDHeading(f'Result of {msl:s} for {self.loadcase:s} ({lctyp:s})', 3)
        mdstr += str(heading)
        table = MDTable()
        table.add_column(f'y ({config.lunit:s})', config.l1frm)
        table.add_column(f'z ({config.lunit:s})', config.l1frm)
        table.add_column(f'y<sub>na</sub> ({config.lunit:s})', config.l1frm)
        table.add_column(f'z<sub>na</sub> ({config.lunit:s})', config.l1frm)
        table.add_column('&epsilon;', '.6f')
        table.add_column(f'&sigma; ({config.sunit:s})', '.1f')
        table.add_column(f'Allowed ({config.sunit:s})', '.1f')
        if config.msmode:
            table.add_column('MS', '.2f')
        else:
            table.add_column('RF', '.2f')
        for i, resi in enumerate(self.result):
            if resi != float('inf'):
                resi = floor(resi*100)/100
            if config.msmode:
                resi = resi - 1.0
            table.add_row([self.y[i], self.z[i], self.yna[i], self.zna[i],
                           self.eps[i], self.sigma[i], self.allowed[i], resi])
        mdstr += table.__str__()
        return mdstr

    def __str__(self) -> str:
        lctyp = 'Ultimate'
        if self.limit:
            lctyp = 'Limit'
        msl = self.materialsection.label
        mdstr = ''
        heading = MDHeading(f'Result of {msl:s} for {self.loadcase:s} ({lctyp:s})', 3)
        mdstr += str(heading)
        table = MDTable()
        table.add_column(f'y ({config.lunit:s})', config.l1frm)
        table.add_column(f'z ({config.lunit:s})', config.l1frm)
        table.add_column(f'y_na ({config.lunit:s})', config.l1frm)
        table.add_column(f'z_na ({config.lunit:s})', config.l1frm)
        table.add_column('Strain', '.6f')
        table.add_column(f'Stress ({config.sunit:s})', '.1f')
        table.add_column(f'Allowed ({config.sunit:s})', '.1f')
        if config.msmode:
            table.add_column('MS', '.2f')
        else:
            table.add_column('RF', '.2f')
        for i, resi in enumerate(self.result):
            resi = floor(resi*100)/100
            if config.msmode:
                resi = resi - 1.0
            table.add_row([self.y[i], self.z[i], self.yna[i], self.zna[i],
                           self.eps[i], self.sigma[i], self.allowed[i], resi])
        mdstr += table.__str__()
        return mdstr

    def __repr__(self) -> str:
        return '<SectionResult>'
