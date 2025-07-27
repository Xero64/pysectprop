class Point():
    y: float = None
    z: float = None

    def __init__(self, y: float, z: float) -> None:
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return f'<Point: {self.y:}, {self.z:}>'
