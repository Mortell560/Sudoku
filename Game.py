class Game:
    
    
    def place(self,coords,num):

        val=self.B[coords]
        self.B[coords]=num
        self.last_moves.empiler((coords,val))
