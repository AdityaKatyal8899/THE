from runtime.value import THE_Value

class THE_String(THE_Value):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value
    
    def __str__(self):
        return str(self.value)
    
    
    def add(self, other):
        return THE_String(self.value + other.value)
    
    def equals(self, other):
        return self.value == other.value
    
    
    