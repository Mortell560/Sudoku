from time import sleep
from Window import Window
from Pile import Pile
from Board import Board
import graphics

class Game:
    def __init__(self, n):
        self.last_moves = Pile()
        self.n = n
        self.B = Board()
        self.B.create_board(n)
        self.W = Window(600, 800)
        
    def run(self):
        while graphics.pas_echap():
            if self.B.is_win():
                self.W.affiche_win()
                sleep(10)
                self.B.create_board(self.n) # ne pas oublié le n nombre de case mise dans le jeu
                while not self.last_moves.est_vide():
                    self.last_moves.depiler()

            self.W.afficher(self.B, self.last_moves)
            action = self.W.ask_action(board=self.B) #tuple(tuple(x,y), Action) | None | tuple(None, Action)
            print(action)
            if action[1] == Window.PLACE:
                self.W.affiche_selection(action[0])
                value = self.W.ask_value()
                if value:
                    self.place(action[0], value)

            elif action[1] == Window.RETURN:
                if self.last_moves.est_vide():
                    continue
                else:
                    self.retour()

            elif action[1] == Window.RESET:
                self.B.create_board(self.n) # ne pas oublié le n nombre de case mise dans le jeu
                while not self.last_moves.est_vide():
                    self.last_moves.depiler()

            elif action[1] == Window.SOLVE:
                self.B.solve()
    
    def place(self,coords,num):
        val=self.B[coords]
        self.B[coords]=num
        self.last_moves.empiler((coords,val))

    def retour(self):
        p=self.last_moves.depiler()
        self.B[p[0]]=p[1]
