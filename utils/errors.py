class LexerError(Exception):
    pass

class ParseError(Exception):
    pass

class RuntimeError(Exception):
    pass

class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value

class BreakSignal(Exception):
    pass

class ContinueSignal(Exception):
    pass

class THEerror(Exception):
    def __init__(self, message, type="Runtime Error"):
        self.message = message
        self.type = type
        super().__init__(f"{type}:{message}")

    def __str__(self):
        return f"{self.type}: {self.message}"

  