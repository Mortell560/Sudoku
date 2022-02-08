from Pile import Pile
from datetime import datetime
import graphics
from Board import Board
import os

_PATHS = {
    "Save": "img/Save.png",
    "Arrow" : "img/Arrow.png",
    "Reset": "img/Reset.png",
    "Check": "img/Check.png",
    "Leaderboard": "img/Menu.png",
    "Cross": "img/No.png",
    "Leaderboard_txt": "data/leaderboard.txt",
}

VERSION = "0.1"
PLACE = 0
RETURN = 1
SOLVE = 2
SAVE = 3
RESET = 4
LOAD = 5

class Window:
    """Classe qui s'occupe de l'affichage du sudoku"""

    def __init__(self, length: int, width: int) -> None:
        self.width = width
        self.length = length
        self.begin_point_board = (self.length//5, self.width//3)
        self.taille_case = self.length // 13
        self.offset = 20
        self.num_pad_x = self.length//3 + self.offset * 3 # yes i did tests and it works
        self.num_pad_y = 100
        self.img_size = 64
        graphics.init_fenetre(length, width, 'sudoku')
        graphics.remplir_fenetre(graphics.blanc)
        graphics.affiche_auto_off()


    ########################################### Methodes de conversion ###########################################
    def _board_coord_to_pixel_coord(self, x: int, y: int) -> tuple:
        """ Conversion une coordonnée de plateau en coordonnée en pixel """
        px = x * self.taille_case + self.begin_point_board[0]
        py = y * self.taille_case + self.begin_point_board[1]

        return px, py

    def _pixel_coord_to_board_coord(self, x: int, y: int) -> tuple:
        """ Conversion une coordonnée en pixel en coordonnée de plateau """
        bx = (x - self.begin_point_board[0] + self.offset - 1)  // self.taille_case
        by = (y - self.begin_point_board[1] - 1) // self.taille_case

        return bx, by

    def _pixel_coord_to_num_pad_coord(self, x: int, y: int) -> tuple:
        """ Convertion une coordonnée en pixel en coordonnée du num pad """
        bx = (x - self.num_pad_x + self.offset - 1) // self.taille_case
        by = (y - self.num_pad_y - 1) // self.taille_case

        return bx, by

    ########################################### Methodes de verification ###########################################
    def is_in_board(self, x: int, y: int) -> bool:
        """Vérifie si les coordonnées passées en paramètre sont dans la grille"""
        return self.begin_point_board[0] - self.offset <= x <= self.begin_point_board[0] + self.taille_case * 9 - self.offset and \
            self.begin_point_board[1] <= y <= self.begin_point_board[1] + self.taille_case * 9

    def is_in_num_pad(self, x: int, y: int) -> bool:
        """Vérifie si les coordonnées passées en paramètre sont dans le num pad"""
        return self.num_pad_x - self.offset <= x <= self.num_pad_x + 3 * self.taille_case - self.offset and \
            self.num_pad_y <= y <= self.num_pad_y + self.taille_case * 3

    def is_in_leaderboard(self, x: int, y: int) -> bool:
        """Vérifie si les coordonnées passées en paramètre sont sur le bouton de leaderboard"""
        return self.offset//2 <= x <= self.img_size+self.offset//2 and \
            self.width - 75 <= y <= self.width - 75 + self.img_size
            
    def is_in_save_button(self, x: int, y: int) -> bool:
        """Vérifie si les coordonnées passées en paramètre sont sur le bouton de sauvegarde"""
        return self.img_size <= x <= self.img_size * 2 and \
            self.img_size + self.offset * 5 <= y <= self.offset * 5 + self.img_size * 2

    def is_in_arrow_button(self, x: int, y: int) -> bool:
        """Vérifie si les coordonnées passées en paramètre sont sur le bouton de retour en arriere"""
        return self.length - self.offset * 5 <= x <= self.length - self.offset * 5 + self.img_size and \
           self.offset * 5 + self.img_size <= y <= self.offset * 5 + self.img_size * 2

    def is_in_solve_button(self, x: int, y: int) -> bool:
        """Vérifie si les coordonnées passées en paramètre sont sur le bouton de résolution"""
        return self.length - self.img_size - self.offset * 2 <= x <= self.length - self.offset * 2 and \
            self.img_size <= y <= self.img_size*2

    def is_in_cancel_button(self, x: int, y: int) -> bool:
        """Vérifie si les coordonnées passées en paramètre sont sur le bouton pour annuler la selection d'une valeur"""
        return self.length - 100 <= x <= self.length - 100 + self.img_size and \
            self.width - 100 <= y <= self.width - 100 + self.img_size
    
    def is_in_reset_button(self, x: int, y: int) -> bool:
        """Vérifie si les coordonnées passées en paramètre sont sur le bouton de reset"""
        return self.img_size <= x <= self.img_size*2 and \
            self.img_size <= y <= self.img_size*2

    ########################################### Getters ###########################################
    def ask_value(self):
        """Waits for a click and returns the value that must be assigned to the cell"""
        self.affiche_num_pad()
        self._affiche_cancel_button()
        x, y = graphics.wait_clic()
        
        cancelled = self.is_in_cancel_button(x, y)

        # Tant que le clic n'est pas dans le num pad ou cancelled, on redemande un clic
        while not self.is_in_num_pad(x, y) and not cancelled:
            x, y = graphics.wait_clic()
            cancelled = self.is_in_cancel_button(x, y)
        
        self._clear()

        if cancelled:
            return None
        
        x, y = self._pixel_coord_to_num_pad_coord(x, y)
        return x + y * 3 + 1

    def ask_action(self, board: Board):
        """Waits for a click and returns the coordinates of the click and the action associated with it"""
        x, y = graphics.wait_clic()
        Action = PLACE

        # Tant que le clic n'est pas dans la grille, dans l'un des différents boutons, on redemande un clic
        in_board = self.is_in_board(x, y)
        in_leaderboard = self.is_in_leaderboard(x, y)
        in_save = self.is_in_save_button(x, y)
        in_arrow = self.is_in_arrow_button(x, y)
        in_solve = self.is_in_solve_button(x, y)
        in_reset = self.is_in_reset_button(x, y)

        while not in_board and not in_leaderboard and not in_save and not in_arrow and not in_solve and not in_reset:
            x, y = graphics.wait_clic()
            in_board = self.is_in_board(x, y)
            in_leaderboard = self.is_in_leaderboard(x, y)
            in_save = self.is_in_save_button(x, y)
            in_arrow = self.is_in_arrow_button(x, y)
            in_solve = self.is_in_solve_button(x, y)
            in_reset = self.is_in_reset_button(x, y)

        if in_board:
            Action = PLACE
            return self._pixel_coord_to_board_coord(x, y), Action

        elif in_leaderboard:
            self.affiche_leaderboard()
            return None, -1

        elif in_save:
            Action = SAVE
            #self.load_board(board)
            #self.save_leaderboard(6, "Rotate", board)
            return None, Action
        
        elif in_arrow:
            Action = RETURN
            return None, Action
        
        elif in_solve:
            Action = SOLVE
            return None, Action

        else:
            Action = RESET
            return None, Action


    ########################################### Methodes d'affichage ###########################################
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
                    if not board.check_cell((j, i), board[(j, i)]):
                        self._afficher_case_err((j, i))

                    graphics.affiche_texte(str(board[(j, i)]), (self.begin_point_board[0] + self.taille_case * j, self.begin_point_board[1] + self.taille_case * i), couleur=graphics.noir, taille_police=35, police='Arial')
    
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
                graphics.affiche_texte(list_n[x+y*3], (self.num_pad_x + x * self.taille_case, self.num_pad_y + y * self.taille_case), couleur=graphics.noir, taille_police=35, police='Arial')
        graphics.affiche_tout()

    def affiche_leaderboard(self) -> None:
        self._clear()
        graphics.affiche_texte(f"Sudoku V{VERSION}", (self.length//2 - 150, self.width - 100), couleur=graphics.noir, taille_police=50, police='Comic Sans MS')

        l = self.load_leaderboard()
        l.sort(key=lambda x: x[1]) # Trie de la liste des scores par ordre décroissant en fonction du nombre de coup
        if len(l) > 15:
            l = l[:15] # On ne garde que les 15 premiers scores
        
        for i, value in enumerate(l):
            graphics.affiche_texte(f"{value[0]} : {value[1]} moves - {value[2]}", (self.length//2 - 250, self.width - 150 - i * 50), couleur=graphics.noir, taille_police=35, police='Arial')
        
        graphics.affiche_tout()
        graphics.wait_clic()
        self._clear()
    
    def _affiche_icon_and_buttons(self, pile: Pile) -> None:
        self.affiche_image_wrapper(_PATHS["Arrow"], (self.length - self.offset * 5, self.img_size + self.offset * 5)) # Affichage de l'icone de la flèche pour le retour en arrière
        self.affiche_image_wrapper(_PATHS["Save"], (self.img_size, self.img_size + self.offset * 5)) # Affichage de l'icone de sauvegarde du score
        self.affiche_image_wrapper(_PATHS["Reset"], (self.img_size, self.img_size)) # Affichage de l'icone de réinitialisation du problème
        self.affiche_image_wrapper(_PATHS["Check"], (self.length - self.img_size - self.offset * 2, self.img_size)) # Affichage de l'icone pour solve le problème
        self.affiche_image_wrapper(_PATHS["Leaderboard"], (10, self.width - 75)) # Affichage de l'icone pour afficher le leaderboard
        graphics.affiche_texte(str(len(pile)), (self.length - self.offset * 3 - self.offset//2, self.img_size + self.offset * 5 - self.offset), couleur=graphics.noir, taille_police=35, police='Arial')

    def afficher(self, board: list, pile_coup_joue: Pile = []) -> None:
        """Affiche tout le jeu"""
        self.affiche_tableau(board)
        graphics.affiche_texte(f"Sudoku V{VERSION}", (self.length // 2 - 150, self.width - 100), couleur=graphics.noir, taille_police=50, police='Comic Sans MS') # Affiche le titre du jeu et la version
        self._affiche_icon_and_buttons(pile_coup_joue)
        graphics.affiche_tout()

    def affiche_win(self) -> None:
        """Affiche le message de victoire"""
        graphics.affiche_texte("Gagné !", (self.num_pad_x + self.offset * 2 + 5, self.num_pad_y + self.taille_case * 3 + self.offset), couleur=graphics.rouge, taille_police=35, police='Arial')
        graphics.affiche_tout()

    def _affiche_cancel_button(self) -> None:
        self.affiche_image_wrapper(_PATHS["Cross"], (self.length - 100, self.width - 100)) # Affichage de l'icone de la croix pour cancel son choix
        graphics.affiche_tout()
    
    def affiche_selection(self, coords):
        """Affiche le rectangle de sélection"""
        x, y = coords
        graphics.affiche_rectangle((self.begin_point_board[0] + x * self.taille_case - self.offset+1, self.begin_point_board[1] + y * self.taille_case), \
            (self.begin_point_board[0] + (x+1) * self.taille_case - self.offset, self.begin_point_board[1] + (y+1) * self.taille_case - 1), couleur=graphics.vert, epaisseur=3)
        graphics.affiche_tout()

    ########################################### Wrappers, fonctions utilitaires ###########################################
    def _clear(self):
        graphics.remplir_fenetre(graphics.blanc)

    def _afficher_case_err(self, coords):
        x, y = coords
        graphics.affiche_rectangle_plein((self.begin_point_board[0] + x * self.taille_case - self.offset+1, self.begin_point_board[1] + y * self.taille_case), \
            (self.begin_point_board[0] + (x+1) * self.taille_case - self.offset, self.begin_point_board[1] + (y+1) * self.taille_case - 1), couleur=graphics.rouge)

    def affiche_image_wrapper(self, img_path, dest_bas_gauche) -> None:
        """Affiche une image avec son path et la position du point le plus bas à gauche de l'image"""
        try:
            graphics.affiche_image(img_path, dest_bas_gauche)
        except FileNotFoundError:
            err_msg = """
            Le fichier "{}" n\'a pas pu être ouvert depuis le dossier actuel "{}"
            Verifiez que le dossier l'image est présente et lancez le jeu depuis le dossier src/
            """.format(img_path, os.getcwd())

            print(err_msg)
            exit(1)

    def load_board(self) -> None:
        try:
            with open(_PATHS["Leaderboard_txt"], 'r') as f:
                last_save = f.readlines()[-1].strip().split(',')[3:]
                return last_save

        except FileNotFoundError:
            err_msg = """
            Le fichier "{}" n\'a pas pu être ouvert depuis le dossier actuel "{}"
            Verifiez que le dossier data est présent et lancez le jeu depuis le dossier src
            """.format(_PATHS["Leaderboard_txt"], os.getcwd())

            print(err_msg)
            exit(1)

    def load_leaderboard(self) -> list:
        try:
            with open(_PATHS["Leaderboard_txt"], 'r') as f:
                l = []
                lines = f.readlines()
                for line in lines:
                    line = line.strip().split(',')
                    l.append((line[0], int(line[1]), line[2]))
                return l

        except FileNotFoundError:
            err_msg = """
            Le fichier "{}" n\'a pas pu être ouvert depuis le dossier actuel "{}"
            Verifiez que le dossier data est présent et lancez le jeu depuis le dossier src
            """.format(_PATHS["Leaderboard_txt"], os.getcwd())

            print(err_msg)
            exit(1)

    def save_leaderboard(self, score: int, username: str, board: Board) -> None:
        """Sauvegarde les stats d'username et son score (nb moves) ainsi que le board dans le fichier leaderboard.txt"""
        try:
            liste_str = board.__str__()
            now = datetime.now()
            date = now.strftime("%d/%m/%Y %H:%M:%S")
            with open(_PATHS["Leaderboard_txt"], 'a') as f:
                f.write(f"{username},{score},{date},{liste_str}\n")
        except FileNotFoundError:
            err_msg = """
            Le fichier "{}" n\'a pas pu être ouvert depuis le dossier actuel "{}"
            Verifiez que le dossier data est présent et lancez le jeu depuis le dossier src
            """.format(_PATHS["Leaderboard_txt"], os.getcwd())

            print(err_msg)
            exit(1)
        
###################### Partie Test ##############################

b= Board()
b.board=[0]*9*9
b[4, 7] = 5
b[5, 5] = 6
b[4, 3] = 5
a = Window(600, 800)
while graphics.pas_echap():
    a.afficher(b)
    x = a.ask_action(b)
    print(x)
    if x and x[1] == PLACE:
        a.affiche_selection(x[0])
        y = a.ask_value()
        if y:
            b[x[0][0], x[0][1]] = y

