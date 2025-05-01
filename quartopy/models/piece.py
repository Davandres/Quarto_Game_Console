from enum import Enum

class Coloration(Enum):
    BEIGE = "BEIGE"
    BROWN = "BROWN"

class Shape(Enum):
    CIRCLE = "CIRCLE"
    SQUARE = "SQUARE"

class Size(Enum):
    TALL = "TALL"
    LITTLE = "LITTLE"

class Hole(Enum):
    WITH = "WITH_HOLE"
    WITHOUT = "WITHOUT_HOLE"

class Piece:
    def __init__(self, row, col, coloration, shape, size, hole):
        if not isinstance(coloration, Coloration):
            raise ValueError("coloration must be a Coloration enum")
        if not isinstance(shape, Shape):
            raise ValueError("shape must be a Shape enum")
        if not isinstance(size, Size):
            raise ValueError("size must be a Size enum")
        if not isinstance(hole, Hole):
            raise ValueError("hole must be a Hole enum")
            
        self.row = row
        self.col = col
        self.coloration = coloration
        self.shape = shape
        self.size = size
        self.hole = hole

    def __repr__(self, verbose=False):
        if verbose:
            return f"{self.size.value}, {self.coloration.value}, {self.shape.value}, {self.hole.value}"
        else:
            return (f"{'T' if self.size == Size.TALL else 'S'}"
                    f"{'B' if self.coloration == Coloration.BEIGE else 'D'}"
                    f"{'C' if self.shape == Shape.CIRCLE else 'Q'}"
                    f"{'H' if self.hole == Hole.WITH else 'N'}")

    def copy(self):
        """Crea una copia de la pieza"""
        return Piece(self.row, self.col, self.coloration, self.shape, self.size, self.hole)