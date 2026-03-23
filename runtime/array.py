from runtime.value import THE_Value
from utils.errors import THEerror
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
    

    def remove(self, other):
        for i, v in enumerate(self.values):
            if v.value == other.value:
                self.values.pop(i)
                return self

        return self

    def removeAt(self, other):
        idx = other.value

        if idx < 0 or idx >= len(self.values):
            raise THEerror("Index out of range")
        
        return self.values.pop(idx)