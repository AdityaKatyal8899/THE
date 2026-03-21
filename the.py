import sys
from lexer.tokenizer import Tokenizer
from parser.parser import Parser
from Interpreter.interpreter import Interpreter
from utils.errors import THEerror


def run_file(filepath):
    with open(filepath) as f:
        code = f.read()

    lexer = Tokenizer(code)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.program_Parser()

    interpreter = Interpreter()
    interpreter.run(ast)


def main():
    try:
        args = sys.argv

        if len(sys.argv) == 1:
            print("THE language CLI")
            print("Usage: the <file.the>")
            return

        cmd = args[1]

        if cmd in ["--version" or "-v"]:
            print("THE v0.1.0")
            return 
        
        if cmd in ["--help"]:
            print("Usage")
            print("the <filename>.the               Run a THE file")
            print("the --version or the -v          Show version")
            print("the --help               Show CLI commands")

            return 
        
        run_file(cmd)

    except Exception as e:
        if not isinstance(e, THEerror):
            e = THEerror(str(e))
        print(e)


if __name__ == "__main__":
    main()