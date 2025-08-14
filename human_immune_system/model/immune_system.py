class ImmuneSystem:
    def __init__(self):
        self.immune_activation = False
    
    def antigen_exposure(self, antigen):
        if antigen:
            self.immune_activation = True
            return True
        return False
    
    def is_activated(self):
        return self.immune_activation
