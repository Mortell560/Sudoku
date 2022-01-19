import graphics
from Board import Board
class Window:
    def __init__(self, length: int, width: int) -> None:
        self.width = width
        self.length = length
        graphics.init_fenetre(length, width, 'sudoku')

    def ask_move(self):
        pass
        
    def affiche_tableau(self, board: Board):
        pass
    
    def afficher(self, board: list) -> None:
        graphics.affiche_auto_off()
        self.affiche_tableau()
        graphics.affiche_tout()
        
###################### Partie Test ##############################
a = Window(1000, 1000)
