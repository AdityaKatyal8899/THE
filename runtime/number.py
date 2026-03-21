from runtime.value import THE_Value
from runtime.boolean import THE_Boolean
from utils.errors import THEerror
class THE_Number(THE_Value):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)
    
    def __str__(self):
        return str(self.value)

    def add(self, other):
        return THE_Number(self.value + other.value)
    
    def subtract(self, other):
        return THE_Number(self.value - other.value)
    
    def multiply(self, other):
        return THE_Number(self.value * other.value)
    
    def divide(self, other):
        try:
            return THE_Number(self.value / other.value)
        
        except ZeroDivisionError:
            raise THEerror("Division by zero")
    
    def modulo(self, other):
        return THE_Number(self.value % other.value)
    
    def greater(self, other):
        return THE_Boolean(self.value > other.value)
    
    def lesser(self, other):
        return THE_Boolean(self.value < other.value)
    
    def greaterOrEqual(self, other):
        return THE_Boolean(self.value >= other.value)
    
    def lessOrEqual(self, other):
        return THE_Boolean(self.value <= other.value)
    
    def equals(self, other):
        return THE_Boolean(self.value == other.value)
    