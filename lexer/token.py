# keywords
INT = "INT"
BINT = "BINT"
FLO = "FLO"
STR = "STR"
BOOL = "BOOL"
CHAR = "CHAR"
IF ="IF"
ELSE ="ELSE"

COMMA = "COMMA"
COLON = "COLON"
LPAREN = "LPAREN"
RPAREN = "RPAREN"
LBRACE = "LBRACE"
RBRACE = "RBRACE"
LBRACKET = "LBRACKET"
RBRACKET = "RBRACKET"

DOT = "DOT"
WITH = "WITH"

GET = "GET"
GIVE = "GIVE"

TRUE = "TRUE"
FALSE = "FALSE"

# identifiers and literals
IDENTIFIER = "IDENTIFIER"
NUMBER = "NUMBER"
STRING = "STRING"

STOP = "STOP"
NEXT = "NEXT"
IDLE = "IDLE"

# operators
PLUS = "PLUS"
MINUS = "MINUS"
MULTIPLY = "MULTIPLY"
DIVIDE = "DIVIDE"
ASSIGN = "ASSIGN"
MODULO = "MODULO"
AND = "AND"
OR= "OR"
NOT = "NOT"

#loops
LOOPTILL = "LOOPTILL"
LOOPIN = "LOOPIN"

#function
FUNC = "FUNC"

#retur nstatement 
RETURN = "RETURN"

#comparison operators
EQ = "EQ"     # ==
GT = "GT"     # >
LT = "LT"     # <
GTE = "GTE"   # >=
LTE = "LTE"   # <=
NEQ = "NEQ"

OPERATORS = {
    "==": EQ,
    ">=": GTE,
    "<=": LTE,
    "!=": NEQ,
    ">": GT,
    "<": LT,
    "=": ASSIGN,
    "+": PLUS,
    "-": MINUS,
    "*": MULTIPLY,
    "/": DIVIDE,
    "%": MODULO,
    "&&": AND,
    "||": OR,
    "!": NOT,

}

# structure
NEWLINE = "NEWLINE"
EOF = "EOF"

TRY = "TRY"
CATCH = "CATCH"
THROW = "THROW"
RAISE = "RAISE"

KEYWORDS ={
    "INT": INT,
    "BINT": BINT,
    "FLO": FLO,
    "STR": STR,
    "BOOL": BOOL,
    "CHAR": CHAR,

    "get": GET,
    "give": GIVE,

    "true": TRUE,
    "false": FALSE,
    "False": FALSE,
    "True": TRUE,

    "if": IF,
    "else": ELSE,

    "and": AND,
    "or": OR,
    "not": NOT,
    "LoopTill": LOOPTILL,
    "LoopIn": LOOPIN,
    "with": WITH,
    "try": TRY,
    "catch": CATCH,
    "func" or "function" : FUNC,
    "return": RETURN,
    "next": NEXT,
    "stop": STOP,
    "idle": IDLE,

    "throw": THROW,
    "raise": RAISE,
    
}

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.value is None:
            return f"{self.type}"
        
        else:
            return f"{self.type}({self.value})"
        

        

