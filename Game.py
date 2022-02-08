class Game:
    
    
    def place(self,coords,num):

        val=self.B[coords]
        self.B[coords]=num
        self.empiler.last_moves((coords,val))
