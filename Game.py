class Board:
    def __init__(self):
        self.board = []
        self.colonne = 9
        self.ligne = 9
        self.taille_case = 3

    def check_col(self,coords):#regarde si y'a un autre chiffre égal sur toute la même colonne
        x, y = coords[0], coords[1]
        for colonne in range(self.colonne):
            if colonne == y:
                return False

    def check_ligne(self, coords):#regarde si y'a un autre chiffre égal sur toute la même ligne
        x, y = coords[0], coords[1]
        for colonne in range(self.ligne):
            if colonne == y:
                return False
