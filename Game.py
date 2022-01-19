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
            if colonne == x:
                return False
            
   def get_coords_case(self, coords): #return une liste de tuple de coordonnées qui sont dans la même case que les coordonnées passés en argument
    x, y = coords[0], coords[1]
    liste_coords_case = []
    x_case = x // self.taille_case
    y_case = y // self.taille_case
    for i1 in range(self.taille_case):
        for i2 in range(self.taille_case):
            liste_coords_case.append((x_case + i1, y_case + i2))
    return liste_coords_case
