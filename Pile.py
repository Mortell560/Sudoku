class Pile:
    def __init__(self):
        # initialise une pile vide en tant que liste python
        self.contenu = []

    def est_vide(self):
        # retourne vrai si la pile est vide ou faux sinon
        if self.contenu == []:
            return True
        else:
            return False

    # def est_vide(self):
    # retourne vrai si la pile est vide ou faux sinon
    #    return self.contenu == None

    def empiler(self, elmt):
        # ajoute "elmt" en derniere position
        self.contenu.append(elmt)

    def depiler(self):
        # retourne et enleve l'element qui est en derniere position si la pile n'est pas vide
        if self.est_vide() == False:
            return self.contenu.pop()

    def __len__(self):
        # retourne le nombre d'elements de la pile
        return len(self.contenu)
"""
P = Pile()

nbr1 = P.len()
print(nbr1)

P.empiler(5)

P.empiler(3)

nbr2 = P.len()
print(nbr2)

dernier_elmt_eneleve = P.depiler()
print(dernier_elmt_eneleve)

nbr3 = P.len()
print(nbr3)

k = P.est_vide()
print(k)
"""