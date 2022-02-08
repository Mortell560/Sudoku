class Game:
    
    def place(self,coords,num):
        val=self.B[coords]
        self.B[coords]=num
        self.last_moves.empiler((coords,val))

    def retour(self):
        p=self.last_move.depiler()
        self.B[p[0]]=p[1]