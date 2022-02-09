from Window import Window
from Pile import Pile
from Board import Board

class Game:
    def __init__(self, n):
        self.last_moves = Pile()
        self.W = Window(600, 800)
        self.n = n
        self.B = Board(n)
        
    def run(self):
        while self.graphics.pas_echap():
            self.W.afficher(self.B)
            action = self.W.ask_action() #tuple(tuple(x,y), Action) | None | tuple(None, Action)
            if action[1] == self.W.PLACE:
                value = self.W.ask_value()
                self.place(action[0], value)

            elif action[1] == self.W.RETURN:
                if self.last_moves.est_vide():
                    continue
                else:
                    self.retour()

            elif action[1] == self.W.RESET:
                self.B.create_board(self.n) # ne pas oublié le n nombre de case mise dans le jeu
                while not self.last_moves.est_vide():
                    self.last_moves.depiler()

            elif action[1] == self.W.SOLVE:
                self.B.solve()
    
    def place(self,coords,num):
        val=self.B[coords]
        self.B[coords]=num
        self.last_moves.empiler((coords,val))

    def retour(self):
        p=self.last_move.depiler()
        self.B[p[0]]=p[1]
