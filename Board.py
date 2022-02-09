import random

class Board:
    ind_liste = 0 #utile pour le create_board()
    def __init__(self):
        self.board = []
        self.colonne = 9
        self.ligne = 9
        self.taille_case = 3

    def create_board(self, n):
        """création dubune remplie de 0 puis on ajoute aléatoirement un certain nombre n"""
        nbr_de_zero = self.colonne * self.ligne
        self.board = nbr_de_zero * [0]

        for nombre in range(n):
            x = random.randint(0,8)
            y = random.randint(0,8)
            nombre_random = random.randint(1,9)
            if self.check_cell((x,y), nombre_random):
                self[x, y] = nombre_random
    
    def __setitem__(self,coords,valeur):
        x,y=coords[0],coords[1]
        indice=x+y*self.colonne
        self.board[indice]=valeur
        
    
    def __getitem__(self,coords):
        x,y=coords[0],coords[1]
        indice=x+y*self.colonne
        return self.board[indice]
    
    def check_colonne(self,coords, value): 
        """regarde si y'a un autre chiffre égal sur toute la même colonne"""
        x, y = coords[0], coords[1]

        for colonne in range(self.colonne):
            if colonne == y:
                continue
            else:
                value_coords_act = self[(x, colonne)]
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
                value_coords_act = self[(ligne, y)]
                if value_coords_act == value:
                    return False
        return True
    
            
    def get_coords_case(self, coords): 
        """return une liste de tuple de coordonnées qui sont dans la même case que les coordonnées passés en argument"""
        x, y = coords[0], coords[1]
        liste_coords_case = []
        x_case = x // self.taille_case * 3
        y_case = y // self.taille_case * 3
        for i1 in range(self.taille_case):
            for i2 in range(self.taille_case):
                liste_coords_case.append((x_case + i1, y_case + i2))
        return liste_coords_case

    def check_case(self,coords: tuple, value: int):
        # verifie pour le carre de 9 cases (ou se trouvent les coords)si "value" est deja present
        #si jamais value est present on retourne false sinon True
        liste=self.get_coords_case(coords)
        for coord in liste:
            if self[coord] == value and coord != coords:
                return False
        return True

    def check_cell(self, coords, value):
        """utilise tous les précédents checks pour déterminer si la position est complètement valide. True si c’est le cas, False sinon."""
        return self.check_colonne(coords, value) and self.check_ligne(coords, value) and self.check_case(coords, value)

    def coord_to_list_coord(self, coords):
        x,y=coords[0],coords[1]
        indice=x+y*self.colonne
        return indice
      
    def list_indice_to_coords(self, ind_liste):
        """donne les coords en fonction de l'indice dans la liste self.board"""
        x = ind_liste % 9
        y = ind_liste // 9
        coords = (x,y)
        return coords
        
    def is_empty(self,coords):
        x,y=coords[0],coords[1]
        if self[x,y] == 0 :
            return True
        else: 
            return False
        
    def is_win(self):
        for y in range(self.colonne):
            for x in range(self.ligne):
                if not self.check_cells((x,y),self[x,y]):   
                    return False                
        return True
    
    def is_full(self):    
        for i in self.boards:
            if i == 0:
                return False
            else:
                return True
    
    def __str__(self) -> str:
        string=""
        for val in self.board:
            string += str(val) + ","
        return string[:-1]
    
    def solve(self):
        for x in range(9):
            for y in range(9):
                ind = self.coord_to_list_coord((x,y))
                if self.board[ind] == 0:
                    for valeur in range(1, 10):
                        if self.check_cell((x,y), valeur):
                            self.board[ind] = valeur
                            self.solve()
                            self.board[ind] = 0

