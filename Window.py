import graphics

class Window:
    def __init__(self, length: int, width: int) -> None:
        self.length = length
        self.width = width
        graphics.init_fenetre(length, width, 'sudoku')

#tests
a = Window(500, 500)
