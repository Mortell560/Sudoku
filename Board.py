import random

class Board:
    ind_liste = 0 #utile pour le create_board()
    def __init__(self):
        self.board = []
        self.colonne = 9
        self.ligne = 9
        self.taille_case = 3
    
    def create_board(self, n):
        '''création d'un tableau remplie de 0. Puis on ajoute un nombre n de chiffres aléatoirement dans celui-ci'''
        pass #culture
    
    
    def is_full(self):
        """Retourne True si tous les éléments sont non nuls, Sinon False"""
        pass
    
    
    def check_colonne(self,coords, value): 
        """regarde si y'a un autre chiffre égal sur toute la même colonne"""
        x, y = coords[0], coords[1]
        for colonne in range(self.colonne):
            if colonne == y:
                continue
            else:
                value_coords_act = self.get_value(x, colonne)
                if value_coords_act == value:
                    return False
        return True
                

    def check_ligne(self, coords, value): 
        """regarde si y'a un autre chiffre égal sur toute la même ligne"""
        x, y = coords[0], coords[1]
        for ligne in range(self.ligne):
            if ligne == x:
                continue
            else:
                value_coords_act = self.get_value(ligne, y)
                if value_coords_act == value:
                    return False
        return True
    
    
    def check_case(self, coords: tuple, value: int):
        """Vérifie que la position coords avec la valeur value est valide pour la case. True si oui, Sinon False"""
        return pass
    
    
    def check_cell(self, coords, value):
        """utilise tous les précédents checks pour déterminer si la position est complètement valide. True si c’est le cas, False sinon."""
        return self.check_case(coords, value) and self.check_colonne(coords, value) and self.check_ligne(coords, value)
    
    
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

    
    def coord_to_list_coord(self, coords):
        """donne l'indice de la coords données en argument de la liste self.board"""
        x, y = coords[0], coords[1]
        indice = x + y * self.colonne
        return indice
   

    def list_indice_to_coords(self, ind_liste):
        """donne les coords en fonction de l'indice dans la liste self.board"""
        x = ind_liste % 9
        y = ind_liste // 9
        coords = (x,y)
        return coords
    
    
    def __setitem__(self, coords, valeur):
        """met une valeur aux coords données"""
        x , y = coords[0], coords[1]
        indice = x+ y * self.colonne
        self.board[indice] = valeur
        
    
    def __getitem__(self,coords):
        """donne la valeur en fonction des coords données"""
        x , y = coords[0], coords[1]
        indice = x + y * self.colonne
        return self.board[indice]
