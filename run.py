from lexer.tokenizer import Tokenizer
from parser.parser import Parser
from Interpreter.interpreter import Interpreter
from utils.errors import THEerror

with open("examples/hello.the") as f:
    code = f.read()

lexer = Tokenizer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.program_Parser()

interpret = Interpreter()

try:
    interpret.run(ast)

except Exception as e:
    if isinstance(e, THEerror):
        e = THEerror(e)

    print(e)

