from runtime.value import THE_Value

class THE_Array(THE_Value):
    def __init__(self, values):
        self.values = values

    def __repr__(self):
        return str(self.values)
    
    def index(self, other):
        return self.values[other.value]
    
    def size(self):
        return len(self.values)
    
    def append(self, *value):
        for v in value:
            self.values.append(v)
        return self
    


    