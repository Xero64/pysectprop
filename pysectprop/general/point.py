class Point(object):
    y = None
    z = None
    def __init__(self, y:float, z:float):
        self.y = y
        self.z = z
    def __repr__(self):
        return '<Point: {:}, {:}>'.format(self.y, self.z)
