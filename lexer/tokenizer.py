from lexer.token import *
from parser.ast_nodes import *
from utils.errors import THEerror

class Tokenizer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[0] if self.text else None

    def advance(self):
        self.pos += 1

        if self.pos >= len(self.text):
            self.current_char = None

        else:
            self.current_char = self.text[self.pos]

    def skip_whitespaces(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
              
    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos] 
    
    
    def peek2(self):
        peek_pos = self.pos + 2
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos] 
    
    
    def skip_single_line_comments(self):
        self.advance()
        self.advance()

        while self.current_char is not None and self.current_char != "\t\r\n":
            self.advance()

        if self.current_char == "\n":
            self.advance()
        
    def skip_multi_line_comments(self):
        self.advance()
        self.advance()
        self.advance()
        while self.current_char is not None:
            if self.current_char == "#" and self.peek() == "/" and self.peek2() == "/":
                self.advance()
                self.advance()
                self.advance()
                # return 
            self.advance()
    

    def read_identifiers(self):
        res = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == "_"):
            res += self.current_char

            self.advance()

        return Token( KEYWORDS.get(res, IDENTIFIER), res)

    def read_number(self):

        result = ""
        dot_count = 0

        while self.current_char is not None and (
            self.current_char.isdigit() or self.current_char == "."
        ):

            if self.current_char == ".":
                dot_count += 1

            result += self.current_char
            self.advance()

        if "." in result:
            return Token(NUMBER, float(result))
        else:
            return Token(NUMBER, int(result))
    
    def read_string(self):
        quote = self.current_char
        self.advance()

        result = ""

        while self.current_char is not None and self.current_char != quote:
            result += self.current_char
            self.advance()

        self.advance()

        return Token(STRING, result)


    def tokenize(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespaces()
                continue

            if self.current_char.isalpha() or self.current_char == "_":
                tokens.append(self.read_identifiers())
                continue  

            if self.current_char.isdigit():
                tokens.append(self.read_number())
                continue      
                
            if self.current_char == "[":
                tokens.append(Token(LBRACKET))
                self.advance()
                continue

            if self.current_char == "]":
                tokens.append(Token(RBRACKET))
                self.advance()
                continue

            if self.current_char == ",":
                tokens.append(Token(COMMA))
                self.advance()
                continue

            if self.current_char == ".":
                tokens.append(Token(DOT))
                self.advance()
                continue
                
            if self.current_char == ":":
                tokens.append(Token(COLON))
                self.advance()
                continue
            
            if self.current_char in ['"', "'"]:
                tokens.append(self.read_string())
                continue         

            if self.current_char == "(":
                tokens.append(Token(LPAREN))
                self.advance()
                continue

            if self.current_char == ")":
                tokens.append(Token(RPAREN))
                self.advance()
                continue
            if self.current_char == "{":
                tokens.append(Token(LBRACE, "{"))
                self.advance()
                continue

            if self.current_char == "}":
                tokens.append(Token(RBRACE, "}"))
                self.advance()
                continue

            two_char = self.current_char + (self.peek() or "")

            if two_char in OPERATORS:
                tokens.append(Token(OPERATORS[two_char]))
                self.advance()
                self.advance()
                continue

            if self.current_char in OPERATORS:
                tokens.append(Token(OPERATORS[self.current_char]))
                self.advance()
                continue
            
            raise THEerror(f"ERROR: {repr(self.current_char)}")
        tokens.append(EOF)
        return tokens

                