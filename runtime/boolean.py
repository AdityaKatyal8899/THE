from runtime.value import THE_Value

class THE_Boolean(THE_Value):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return bool(True) if self.value else bool(False)    
    
    def __bool__(self):
        return self.value

    def __str__(self):
        return "True" if self.value else "False"

    def equals(self, other):
        return THE_Boolean(self.value == other.value)

    def andOperation(self, other):
        return THE_Boolean(self.value and other.value)
    
    def orOPeration(self, other):
        return THE_Boolean(self.value or other.value)
    
    def notOperation(self):
        return THE_Boolean(not self.value)


