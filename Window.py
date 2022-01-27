from multiprocessing.connection import wait
from typing import Tuple
from Pile import Pile
import graphics
from Board import Board
import os

_PATHS = {
    "Save": "img/Save.png",
    "Arrow" : "img/Arrow.png"
}

VERSION = "0.1"
PLACE = 0
RETURN = 1
SOLVE = 2
LEADERBOARD = 3

class Window:
    def __init__(self, length: int, width: int) -> None:
        self.width = width
        self.length = length
        self.begin_point_board = (self.length//6, self.width//3)
        self.taille_case = self.length // 13
        self.offset = 20
        self.num_pad_x = self.length//3 + self.offset * 3 # yes i did tests and it works
        self.num_pad_y = 100
        self.img_size = 64
        graphics.init_fenetre(length, width, 'sudoku')
        graphics.remplir_fenetre(graphics.blanc)
        graphics.affiche_auto_off()

    def _board_coord_to_pixel_coord(self, x: int, y: int) -> tuple:
        """ Convertion une coordonnée de plateau en coordonnée en pixel """
        px = x * self.taille_case + self.begin_point_board[0]
        py = y * self.taille_case + self.begin_point_board[1]

        return px, py

    def _pixel_coord_to_board_coord(self, x: int, y: int) -> tuple:
        """ Convertion une coordonnée en pixel en coordonnée de plateau """
        bx = (x - self.begin_point_board[0] + self.offset - 1)  // self.taille_case
        by = (y - self.begin_point_board[1] - 1) // self.taille_case

        return bx, by

    def _pixel_coord_to_num_pad_coord(self, x: int, y: int) -> tuple:
        """ Convertion une coordonnée en pixel en coordonnée du num pad """
        bx = (x - self.num_pad_x + self.offset - 1) // self.taille_case
        by = (y - self.num_pad_y - 1) // self.taille_case

        return bx, by

    def is_in_board(self, x: int, y: int) -> bool:
        """Vérifie si les coordonnées passées en paramètre sont dans la grille"""
        return self.begin_point_board[0] - self.offset <= x <= self.begin_point_board[0] + self.taille_case * 9 - self.offset and \
            self.begin_point_board[1] <= y <= self.begin_point_board[1] + self.taille_case * 9

    def ask_action(self) -> Tuple[Tuple[int, int], int]:
        """Waits for a click and returns the coordinates of the click and the action associated with it"""
        x, y = graphics.wait_clic()
        
        # Tant que le clic n'est pas dans la grille, dans l'un des différents boutons, on redemande un clic
        valid_action = self.is_in_board(x, y)

        while not valid_action:
            x, y = graphics.wait_clic()
            valid_action = self.is_in_board(x, y)
        
        return self._pixel_coord_to_board_coord(x, y), PLACE


    def affiche_tableau(self, board: Board) -> None:
        """Affiche le tableau de sudoku"""

        # Affichage de chaque colonne en faisant attention à l'épaisseur du trait
        for i in range(board.colonne + 1):
            epaisseur = 1
            if i % 3 == 0:
                epaisseur = 3
            graphics.affiche_ligne((self.begin_point_board[0] + i * self.taille_case - self.offset, self.begin_point_board[1]), (self.begin_point_board[0] + i * self.taille_case - self.offset, self.begin_point_board[1] + self.taille_case * 9), graphics.noir, epaisseur)

        # Affichage de chaque ligne en faisant attention à l'épaisseur du trait
        for j in range(board.ligne + 1):
            epaisseur = 1
            if j % 3 == 0:
                epaisseur = 3
            graphics.affiche_ligne((self.begin_point_board[0] - self.offset, self.begin_point_board[1] + j * self.taille_case), (self.begin_point_board[0] + self.taille_case * 9 - self.offset, self.begin_point_board[1] + j * self.taille_case), graphics.noir, epaisseur)

        # Affichage des valeurs non nulles de la grille
        for i in range(board.colonne):
            for j in range(board.ligne):
                if board[(j, i)] != 0:
                    if not board.check_colonne(coords=(j, i), value=board[(j, i)]): # Si la valeur n'est pas valide on l'affiche en rouge || TODO: Penser à mettre check cell au lieu de check colonne
                        graphics.affiche_rectangle_plein((self.begin_point_board[0] + j * self.taille_case - self.offset+1, self.begin_point_board[1] + i * self.taille_case), \
                             (self.begin_point_board[0] + (j+1) * self.taille_case - self.offset, self.begin_point_board[1] + (i+1) * self.taille_case - 1), couleur=graphics.rouge)

                    graphics.affiche_texte(str(board[(j, i)]), (self.begin_point_board[0] + self.taille_case * j + 10, self.begin_point_board[1] + self.taille_case * i + 15), couleur=graphics.noir, taille_police=35, police='Arial')
    
    def affiche_num_pad(self) -> None:
        list_n = [str(i) for i in range(1, 10)] # liste des nombres à afficher

        # Affichage des lignes
        for i in range(4):
            graphics.affiche_ligne((self.num_pad_x - self.offset, self.num_pad_y + i * self.taille_case), (self.num_pad_x + 3 * self.taille_case - self.offset, self.num_pad_y + i * self.taille_case), graphics.noir, epaisseur=3)

        # Affichage des colonnes
        for j in range(4):
            graphics.affiche_ligne((self.num_pad_x + j * self.taille_case - self.offset, self.num_pad_y), (self.num_pad_x + j * self.taille_case - self.offset, self.num_pad_y + self.taille_case * 3), couleur=graphics.noir, epaisseur=3)

        # Affichage des valeurs
        for y in range(3):
            for x in range(3):
                graphics.affiche_texte(list_n[x+y*3], (self.num_pad_x + x * self.taille_case + 10, self.num_pad_y + y * self.taille_case + 15), couleur=graphics.noir, taille_police=35, police='Arial')

    def affiche_leaderboard(self, leaderboard: list[Tuple[str, int]]) -> None:
        graphics.remplir_fenetre(graphics.blanc)
        graphics.affiche_texte(f"Sudoku V{VERSION}", (self.length//2 - 150, self.width - 100), couleur=graphics.noir, taille_police=50, police='Comic Sans MS')
        for i, value in enumerate(leaderboard):
            graphics.affiche_texte(f"{value[0]} : {value[1]}", (self.length//2 - 60, self.width - 150 - i * 50), couleur=graphics.noir, taille_police=35, police='Arial')
        graphics.affiche_tout()
        graphics.wait_clic()
        graphics.remplir_fenetre(graphics.blanc)
    
    def _affiche_icon_and_buttons(self, pile: Pile = []) -> None:
        self.affiche_image_wrapper(_PATHS["Arrow"], (self.length - 200, 300)) # Affichage de l'icone de la flèche pour le retour en arrière
        self.affiche_image_wrapper(_PATHS["Save"], (170, 285)) # Affichage de l'icone de sauvegarde du score
        graphics.affiche_texte(str(len(pile)), (self.length - 170, 250), couleur=graphics.noir, taille_police=35, police='Arial')

    def afficher(self, board: list) -> None:
        self.affiche_tableau(board)
        graphics.affiche_texte(f"Sudoku V{VERSION}", (self.length // 2 - 150, self.width - 100), couleur=graphics.noir, taille_police=50, police='Comic Sans MS') # Affiche le titre du jeu et la version
        #self.affiche_num_pad()
        self._affiche_icon_and_buttons()
        graphics.affiche_tout()

    def affiche_win(self) -> None:
        graphics.affiche_texte("Gagné !", (self.num_pad_x + self.offset * 2 + 5, self.num_pad_y + self.taille_case * 3 + self.offset), couleur=graphics.rouge, taille_police=35, police='Arial')
        graphics.affiche_tout()

    def affiche_image_wrapper(self, img_path, dest_bas_gauche) -> None:
        try:
            graphics.affiche_image(img_path, dest_bas_gauche)
        except FileNotFoundError:
            err_msg = """
            Le fichier "{}" n\'a pas pu être ouvert depuis le dossier actuel "{}"
            Verifiez que le dossier l'image est présente et lancez le jeu depuis le dossier src/
            """.format(img_path, os.getcwd())

            print(err_msg)
            exit(1)

        
###################### Partie Test ##############################
b= Board()
b.board=[0]*9*9
b[4, 7] = 5
b[5, 5] = 6
b[4, 3] = 5
a = Window(1000, 1200)
while graphics.pas_echap():
    a.afficher(b)
    print(a.ask_action())
