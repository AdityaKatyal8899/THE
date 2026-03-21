from runtime.value import THE_Value

class THE_Map(THE_Value):
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return str(self.data)
    
    def get(self, key):
        return self.data[key]
    
    def keys(self):
        return list(self.data.keys())

    def values(self):
        return list(self.data.values())