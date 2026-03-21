from runtime.value import THE_Value

class THESet(THE_Value):
    def __init__(self, values):
        self.values = set(values)

    def __repr__(self):
        return str(self.values)

    def contain(self, value):
        return value in self.values
    
    def size(self):
        return len(self.values)
    
    