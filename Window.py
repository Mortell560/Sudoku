import graphics
from Board import Board
class Window:
    def __init__(self, length: int, width: int) -> None:
        self.width = width
        self.length = length
        graphics.init_fenetre(length, width, 'sudoku')

    def show_menu(self):
        graphics.affiche_texte("Sudoku", (self.width - 100, self.length // 2 - 50), taille=50, couleur=graphics.noir)

    def ask_move(self):
        """Waits for a click and returns the coordinates of the click"""
        coords = graphics.wait_clic()
        pass


    def affiche_tableau(self, board: Board):
        pass
    
    def afficher(self, board: list) -> None:
        graphics.affiche_auto_off()
        self.affiche_tableau()
        graphics.affiche_tout()
        
###################### Partie Test ##############################
a = Window(1000, 1000)
a.show_menu()