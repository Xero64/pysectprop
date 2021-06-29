from math import floor
from py2md.classes import MDHeading, MDTable
from .. import config

class SectionResult(object):
    loadcase: str = None
    limit: bool = None
    msmode: bool = None
    totalsection = None
    materialsection = None
    Fx: float = None
    My: float = None
    Mz: float = None
    y = None
    z = None
    yna = None
    zna = None
    eps = None
    allowed = None
    sigma = None
    result = None
    def __init__(self, materialsection, totalsection=None):
        self.materialsection = materialsection
        if totalsection is None:
            self.totalsection = materialsection
        else:
            self.totalsection = totalsection
        self.msmode = False
    def set_load(self, loadcase, Fx, My, Mz, limit: bool=False):
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
        E = self.materialsection.material.E
        EA = self.totalsection.EA
        EIyy = self.totalsection.EIyy
        EIzz = self.totalsection.EIzz
        EIyz = self.totalsection.EIyz
        cy = self.totalsection.cy
        cz = self.totalsection.cz
        kd = EIyy*EIzz-EIyz**2
        ky = (Mz*EIyy-My*EIyz)/kd
        kz = (My*EIzz-Mz*EIyz)/kd
        self.y, self.z = [], []
        self.yna, self.zna = [], []
        self.eps = []
        self.allowed = []
        self.sigma = []
        self.result = []
        for point in self.materialsection.pnts:
            self.y.append(point.y)
            self.z.append(point.z)
            yna = point.y-cy
            zna = point.z-cz
            self.yna.append(yna)
            self.zna.append(zna)
            eps = Fx/EA+ky*yna+kz*zna
            self.eps.append(eps)
            sigma = eps*E
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
    def __str__(self):
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
        table.add_column(f'y<sub>NA</sub> ({config.lunit:s})', config.l1frm)
        table.add_column(f'z<sub>NA</sub> ({config.lunit:s})', config.l1frm)
        table.add_column('&epsilon;', '.6f')
        table.add_column(f'&sigma; ({config.sunit:s})', '.1f')
        table.add_column(f'Allowed ({config.sunit:s})', '.1f')
        if config.msmode:
            table.add_column('MS', '.2f')
        else:
            table.add_column('RF', '.2f')
        for i, resi in enumerate(self.result):
            resi = floor(resi*100)/100
            if config.msmode:
                resi = resi-1.0
            table.add_row([self.y[i], self.z[i], self.yna[i], self.zna[i],
                           self.eps[i], self.sigma[i], self.allowed[i], resi])
        mdstr += str(table)
        return mdstr
    def _repr_markdown_(self):
        return self.__str__()
