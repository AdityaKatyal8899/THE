from lexer.token import *
from parser.ast_nodes import *
from utils.errors import THEerror 
from lexer.tokenizer import Tokenizer
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = tokens[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]

        else:
            self.current_token = None

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.advance()
        else:
            raise Exception(f"Unexpected token: {self.current_token.type}")

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos >= len(self.tokens):
            return None
        return self.tokens[peek_pos] 
    

    def parse_or(self):
        left = self.parse_and()

        while self.current_token.type == OR:
            operator = self.current_token
            self.eat(OR)
            right = self.parse_and()
            left = BinaryOpNode(left, operator, right)

        return left

    def parse_and(self):
        left = self.parse_not()

        while self.current_token.type == AND:
            operator = self.current_token
            self.eat(AND)
            right = self.parse_not()
            left = BinaryOpNode(left, operator, right)

        return left

    def parse_not(self):
        if self.current_token.type == NOT:
            operator = self.current_token
            self.eat(NOT)
            operand = self.parse_not()
            return UnaryOpNode(operator, operand)

        return self.parse_exp()

    def parse_exp(self):
        left = self.parse_term()

        while self.current_token.type in (PLUS, MINUS, EQ, GT, GTE, LT, LTE):
            operator = self.current_token
            self.eat(operator.type)
            right = self.parse_term()
            left = BinaryOpNode(left, operator, right)

        return left

    def parse_term(self):
        left = self.parse_factor()

        while self.current_token.type in (MULTIPLY, DIVIDE, MODULO):
            operator = self.current_token
            self.eat(operator.type)
            right = self.parse_factor()
            left = BinaryOpNode(left, operator, right)

        return left
    
    def parse_list_elements(self, end_token):
        ele = []

        if self.current_token.type != end_token:
            ele.append(self.parse_or())
            while self.current_token.type == COMMA:
                self.eat(COMMA)
                ele.append(self.parse_or())

        return ele
    def parse_map_elements(self):
        pairs = []

        if self.current_token.type != RBRACE:
            key = self.parse_or()
            self.eat(COLON)
            value = self.parse_or()

            pairs.append((key, value))

            while self.current_token.type == COMMA:
                self.eat(COMMA)
                key = self.parse_or()
                self.eat(COLON)

                value = self.parse_or()
                pairs.append((key,value))

        return pairs

    def parse_factor(self):
        token = self.current_token

        if token.type == GET:
            self.eat(GET)
            self.eat(LPAREN)
            prompt = self.parse_or()
            self.eat(RPAREN)
            node = GetNode(prompt)

        elif token.type == NUMBER:
            self.eat(NUMBER)
            node = NumberNode(token.value)

        elif token.type == STRING:
            self.eat(STRING)
            node = StringNode(token.value)

        elif token.type == IDENTIFIER:
            name = token.value
            self.eat(IDENTIFIER)

            if self.current_token.type == LPAREN:
                self.eat(LPAREN)
                args = []

                if self.current_token.type != RPAREN:
                    args.append(self.parse_or())

                    while self.current_token.type == COMMA:
                        self.eat(COMMA)
                        args.append(self.parse_or())

                self.eat(RPAREN)

                if name == "set":
                    node = SetNode(args)
                else:
                    node = CallNode(name, args)

            else:
                node = IdentifierNode(name)

            #DOT support for inline functions
            while True:
                if self.current_token.type == DOT:
                    self.eat(DOT)

                    method = self.current_token.value
                    self.eat(IDENTIFIER)

                    self.eat(LPAREN)

                    args = []

                    if self.current_token.type != RPAREN:
                        #For single element appending
                        args.append(self.parse_or())

                        #For multiple elements appending
                        while self.current_token.type == COMMA:
                            self.eat(COMMA)
                            args.append(self.parse_or())

                    self.eat(RPAREN)
                    node = MethodCallNode(node, method, args)
                
                elif self.current_token.type == LBRACKET:
                    self.eat(LBRACKET)
                    idx = self.parse_or()
                    self.eat(RBRACKET)

                    node = IndexNode(node, idx)

                else: break

        elif token.type == LBRACE:
            self.eat(LBRACE)

            pairs = self.parse_map_elements()
            
            self.eat(RBRACE)
            node =  MapNode(pairs)

        elif token.type == TRUE:
            self.eat(TRUE)
            node = BooleanNode(True)

        elif token.type == FALSE:
            self.eat(FALSE)
            node = BooleanNode(False)

        elif token.type == LPAREN:
            self.eat(LPAREN)
            elements = self.parse_list_elements(RPAREN)

            if len(elements) > 1:
                node = FrozeListNode(elements)

            else:
                node = elements[0]

            self.eat(RPAREN)


        elif token.type == LBRACKET:
            self.eat(LBRACKET)
            elements = self.parse_list_elements(RBRACKET)
            self.eat(RBRACKET)
            node = ArrayNode(elements)


        elif token.type in (INT, FLO,BINT, STR, CHAR, BOOL):
            name = token.type
            self.eat(token.type)

            self.eat(LPAREN)

            args = []

            if self.current_token.type != RPAREN:
                args.append(self.parse_or())
                while self.current_token == COMMA:
                    self.eat(COMMA) 
                    args.append(self.parse_or())

            self.eat(RPAREN)

            return CallNode(name, args)


        else:
            raise Exception("Invalid factor")

        # POSTFIX INDEXING
        while self.current_token.type == LBRACKET:
            self.eat(LBRACKET)
            index = self.parse_or()
            self.eat(RBRACKET)
            node = IndexNode(node, index)

        return node

    def assignment_parser(self):
        identifier = self.current_token
        self.eat(IDENTIFIER)
        self.eat(ASSIGN)

        value = self.parse_or()

        return AssignNode(
            IdentifierNode(identifier.value),
            value
        )

    def if_parser(self):
        self.eat(IF)

        condition = self.parse_or()

        self.eat(LBRACE)

        true_block = []

        while self.current_token.type != RBRACE:
            true_block.append(self.statement_parser())

        self.eat(RBRACE)

        false_block = None

        if self.current_token.type == ELSE:
            self.eat(ELSE)
            self.eat(LBRACE)

            false_block = []

            while self.current_token.type != RBRACE:
                false_block.append(self.statement_parser())

            self.eat(RBRACE)

        return IfElseNode(condition, true_block, false_block)
    
    def looptill_parser(self):
        self.eat(LOOPTILL)

        if self.current_token and self.current_token.type == LPAREN:
            self.eat(LPAREN)
            condition = self.parse_or()
            self.eat(RPAREN)

        else:
            condition = self.parse_or()
        self.eat(LBRACE)

        body = []

        while self.current_token.type != RBRACE:
            body.append(self.statement_parser())

        self.eat(RBRACE)
        return LoopTillNode(condition, body)
    
    def loopin_parser(self):
        self.eat(LOOPIN)
        it = self.parse_or()

        self.eat(WITH)

        vS = []
        vS.append(self.current_token.value)
        self.eat(IDENTIFIER)

        if self.current_token.type == COMMA:
            self.eat(COMMA)
            vS.append(self.current_token.value)
            self.eat(IDENTIFIER)

        self.eat(LBRACE)

        body = []

        while self.current_token.type != RBRACE:
            body.append(self.statement_parser())
        
        self.eat(RBRACE)
        return LoopInNode(it, vS, body)

    def parse_elements(self):
        ele = []

        if self.current_token.type != LBRACKET:
            ele.append(self.parse_or())
            while self.current_token.type == COMMA:
                self.eat(COMMA)
                ele.append(self.parse_or())

        return ele

    def function_parser(self):
        self.eat(FUNC)

        name = self.current_token.value
        self.eat(IDENTIFIER)

        self.eat(LPAREN)

        params = []

        if self.current_token.type != RPAREN:
            params.append(self.current_token.value)
            self.eat(IDENTIFIER)

            while self.current_token.type == COMMA:
                self.eat(COMMA)
                params.append(self.current_token.value)
                self.eat(IDENTIFIER)

        self.eat(RPAREN)

        self.eat(LBRACE)

        body = []

        while self.current_token.type != RBRACE:
            body.append(self.statement_parser())

        self.eat(RBRACE)

        return FunctionNode(name, params, body)
    
    def function_call_parser(self):
        
        name = self.current_token.value
        self.eat(IDENTIFIER)

        self.eat(LPAREN)

        args = []

        if self.current_token.type != RPAREN:
            args.append(self.parse_or())

            while self.current_token.type == COMMA:
                self.eat(COMMA)
                args.append(self.parse_or())
        self.eat(RPAREN)
        return FunctionCallNode(name, args)
    
    
    def return_parser(self):
        self.eat(RETURN)

        value = None

        if self.current_token and self.current_token.type != RBRACE:
            value = self.parse_or()

        return ReturnNode(value)

    def parse_give(self):
        self.eat(GIVE)
        self.eat(LPAREN)

        value = self.parse_or()

        start = None
        end = None

        while self.current_token.type == COMMA:
            self.eat(COMMA)

            key = self.current_token.value
            self.eat(IDENTIFIER)

            self.eat(ASSIGN)
            val = self.parse_or()
            if key == "start":
                start = val
            
            elif key == "end":
                end = val
            
            else:
                raise Exception("Invalid paramtere in give() statement!")

        self.eat(RPAREN)

        return GiveNode(value, start, end)

    def try_parser(self):
        self.eat(LBRACE)

        try_block = []
        while self.current_token.type != RBRACE and self.current_token.type != EOF:
            if self.current_token.type == RBRACE:
                break
            prev = self.current_token

            stmt = self.statement_parser()
            try_block.append(stmt)

            if self.current_token.type == prev.type and self.current_token.value == prev.value:
                raise Exception("Parser stuck in try block!")

        self.eat(RBRACE)

        catch_block = []

        if self.current_token.type == CATCH:
            self.eat(CATCH)
            err_var = None

            if self.current_token.type == LPAREN:
                self.eat(LPAREN)

                if self.current_token.type == IDENTIFIER:
                    err_var = self.current_token.value
                    self.eat(IDENTIFIER)
                
                else:
                    raise THEerror("Expected identifer in catch() block")
                
                self.eat(RPAREN)

            self.eat(LBRACE)

            while self.current_token.type != RBRACE and self.current_token.type != EOF:
                prev = self.current_token

                stmt = self.statement_parser()
                catch_block.append(stmt)

                if self.current_token.type == prev.type and self.current_token.value == prev.value:
                    raise Exception("Parser stuck in catch block!")

            self.eat(RBRACE)

        return TryCatchNode(try_block, catch_block, err_var)    

    def thorw_parser(self):
        self.eat(LPAREN)

        value = self.parse_or()

        self.eat(RPAREN)

        return ThrowNode(value)            

    def raise_parser(self):
        self.eat(LPAREN)

        value = self.parse_or()

        self.eat(RPAREN)

        return ThrowNode(value)  
    
    def statement_parser(self):
        token = self.current_token
        if token.type == GIVE:
            return self.parse_give()
        
        if token.type == LOOPIN:
            return self.loopin_parser()

        if token.type == IDENTIFIER:
            if self.peek() and self.peek().type == ASSIGN:
                return self.assignment_parser()
            elif self.peek() and self.peek().type == LPAREN:
                return self.function_call_parser()
            else:
                return self.parse_exp()

        if token.type == IF:
            return self.if_parser()
        
        if token.type == LOOPTILL:
            return self.looptill_parser()
        
        if token.type == FUNC:
            return self.function_parser()
    
        if token.type == RETURN:
            return self.return_parser()

        if token.type == STOP:
            self.eat(STOP)
            return StopNode()

        if token.type == NEXT:
            self.eat(NEXT)
            return NextNode()

        if token.type == IDLE:
            self.eat(IDLE)
            return IdleNode()
        
        if token.type == TRY:
            self.eat(TRY)
            return self.try_parser()

        if token.type == THROW:
            self.eat(THROW)
            return self.thorw_parser()
    

        if token.type == RAISE:
            self.eat(RAISE)
            return self.raise_parser()
            
        raise THEerror("Invalid statement")
    

    def program_Parser(self):
        statements = []

        while self.current_token != EOF:
            stmt = self.statement_parser()
            statements.append(stmt)

        return statements