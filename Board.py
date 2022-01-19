class Board:
    def __init__(self):
        self.board = []
        self.colonne = 9
        self.ligne = 9
        self.taille_case = 3

    def check_colonne(self,coords, value): 
        """regarde si y'a un autre chiffre égal sur toute la même colonne"""
        x, y = coords[0], coords[1]
        value_x_y = self.get_value(coords)
        for colonne in range(self.colonne):
            if colonne == y:
                continue
            else:
                value_coords_act = self.get_value(x, colonne)
                if value_coords_act == value_x_y:
                    return False
        return True
                

    def check_ligne(self, coords, value): 
        """regarde si y'a un autre chiffre égal sur toute la même ligne"""
        x, y = coords[0], coords[1]
        value_x_y = self.get_value(coords)
        for ligne in range(self.ligne):
            if ligne == x:
                continue
            else:
                value_coords_act = self.get_value(ligne, y)
                if value_coords_act == value_x_y:
                    return False
        return True
            
    def get_coords_case(self, coords): 
        """return une liste de tuple de coordonnées qui sont dans la même case que les coordonnées passés en argument"""
        x, y = coords[0], coords[1]
        liste_coords_case = []
        x_case = x // self.taille_case
        y_case = y // self.taille_case
        for i1 in range(self.taille_case):
            for i2 in range(self.taille_case):
                liste_coords_case.append((x_case + i1, y_case + i2))
        return liste_coords_case
