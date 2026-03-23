from lexer.token import * 
from runtime.number import THE_Number
from runtime.string import THE_String
from runtime.boolean import THE_Boolean
from runtime.array import THE_Array
from runtime.map import THE_Map 
from runtime.set import THESet
from utils.errors import THEerror
from utils.errors import *



class Interpreter:

    def __init__(self):
        self.env_stack = [{}]
        self.builtin = {
            "append": self.builtin_append,
            "size": self.builtin_size,
            "keys": self.builtin_keys,
            "values": self.builtin_values,
            "contains": self.builtin_contains,
            "range": self.builtin_range,
        }

        self.last_error = None

    #Will give arrays size
    def builtin_size(self, args):
        if len(args) != 1:
            raise Exception("Unsupported!")
        
        obj = args[0]
        return obj.size()
    
    #Will append values in the array
    def builtin_append(self, args):
        if len(args) < 2:
            raise Exception("Unsupoorted!")
        
        return  args[0].append(*args[1: ])

        
    def builtin_range(self, args):
        if len(args) == 1:
            start = 0
            end = args[0].value
            step = 1
        
        elif len(args) == 2:
            start = args[0].value
            end = args[1].value
            step = 1

        elif len(args) == 2:
            start = args[0].value
            end = args[1].value
            step = args[2].value

        else:
            raise THEerror("range expects 1 to 3 arguments")
        
        res=  []
        i = start


        if step == 0:
            raise THEerror("Step can't be 0")
        
        while (step > 0 and i < end) or (step < 0 and i > end):
            res.append(THE_Number(i))
            i += step

        return THE_Array(res)

    #Will give all the keys within the map
    def builtin_keys(self, args):
        if len(args) != 1:
            raise Exception("Unsupported!")
        
        return args[0].keys()
    
    def builtin_values(self, args):
        if len(args) != 1:
            raise Exception("Unsupported!")
        
        return args[0].values()
    
    def builtin_contains(self, args):
        if len(args) != 1:
            raise Exception("Unsupported!")
        
        return args[0].contain(args[1])

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"

        method = getattr(self, method_name)

        return method(node)
    
    def visit_GetNode(self, node):
        prompt = self.visit(node.prompt)
        return THE_String(input(str(prompt)))
    
    def visit_NumberNode(self, node):
        return THE_Number(node.value)

    def visit_StringNode(self, node):
        return THE_String(node.value)
    
    def visit_BooleanNode(self, node):
        return THE_Boolean(node.value)
    
    def visit_IdentifierNode(self, node):
        for env in reversed(self.env_stack):
            if node.name in env:
                return env[node.name]
        raise Exception(f"Undefined value: {node.name}")
    
    def visit_AssignNode(self, node):

        value = self.visit(node.value)

        self.env_stack[-1][node.identifier.name] = value

    def visit_GiveNode(self, node):
        value = self.visit(node.value)

        start = ""
        end = "\n"

        if node.start:
            s = self.visit(node.start)
            start = str(s)

        if node.end:
            e = self.visit(node.end)
            end = str(e)

        print(start + f"{value}", end=end)
    
    def visit_BinaryOpNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.operator.type == PLUS:
            return left.add(right)
        
        if node.operator.type == MINUS:
            return left.subtract(right)
        
        if node.operator.type == MULTIPLY:
            return left.multiply(right)
        
        if node.operator.type == DIVIDE:
            return left.divide(right)
        
        if node.operator.type == MODULO:
            return left.modulo(right)
        
        if node.operator.type == EQ:
            return left.equals(right)

        if node.operator.type == GT:
            return left.greater(right)
        
        if node.operator.type == GTE:
            return left.greaterOrEqual(right)
        
        if node.operator.type == LT:
            return left.lesser(right)
        
        if node.operator.type == LTE:
            return left.lesserOrEqual(right)
        
        if node.operator.type == AND:
            return left.andOperation(right)
        
        if node.operator.type == OR:
            return left.orOperation(right)
        
    def visit_UnaryOpNode(self, node):
        value = self.visit(node.operand)
        if node.operand == NOT:
            return value.notOperation()


    def visit_IfElseNode(self, node):
        cnd = self.visit(node.condition)

        if cnd:
            for i in node.true_block:
                self.visit(i)

        elif node.false_block:
            for i in node.false_block:
                self.visit(i)


    def visit_LoopTillNode(self, node):
        while self.visit(node.condition):
            try:
                for i in node.body:
                    self.visit(i)
            except ContinueSignal:
                continue
                
            except BreakSignal:
                break

    def visit_LoopInNode(self, node):
        itr  = self.visit(node.it)

        #Array traversal
        if hasattr(itr, "values"):

            if len(node.var) != 1:
                raise Exception("LoopIn excepts exactly one variable for arrays!")
            else:
                for item in itr.values:
                    self.env_stack[-1][node.var[0]] = item
                    try:
                        for stmt in node.body:
                            self.visit(stmt)

                    except ContinueSignal:
                        continue
                    
                    except BreakSignal:
                        break

                    except Exception as e:
                        return f"Exception: {e}"

        #Map traversal
        elif hasattr(itr, "data"):

            if len(node.var) != 2:
                raise Exception("LoopIn expects exactly two variable for maps")
            else:
                
                for key, value in itr.data.items():
                    self.env_stack[-1][node.var[0]] = key
                    self.env_stack[-1][node.var[1]] = value
                    try:
                        for stmt in node.body:
                            self.visit(stmt)

                    except ContinueSignal:
                        continue

                    except BreakSignal:
                        break

                    except Exception as e:
                        return f"Exception: {e}"

        else:
            raise Exception("Object not iterable")
                

    def visit_FunctionNode(self, node):
        self.env_stack[-1][node.name] = node

    

    def visit_FunctionCallNode(self, node):
        fun = None
        for env in reversed(self.env_stack):
            if node.name in env:
                fun = env[node.name]
                break

        if not fun:
            raise THEerror(f"Functio'{node.name}' is not defined")
        
        args = [self.visit(arg) for arg in node.args]
    
        if callable(fun):
            return fun(args)
        
        new_env = {}

        for param, val in zip(fun.params, args):
            new_env[param] = val
        
        self.env_stack.append(new_env)

        res = None

        try:
            for stmt in fun.body:
                res = self.visit(stmt)

        finally:
            self.env_stack.pop()

        return res


    def visit_MethodCallNode(self, node):
        obj = self.visit(node.object)
        ar = [self.visit(arg) for arg in node.args]

        method = getattr(obj, node.method)

        return method(*ar)

    def visit_CallNode(self, node):
        if node.name == "INT":
            if len(node.args) != 1:
                raise Exception("INT() expects one argument")
            
            val = self.visit(node.args[0])

            if isinstance(val, THE_Number):
                return THE_Number(int(val.value))
            
            if isinstance(val, THE_String):
                return THE_String(int(val.value))     
                   
            if isinstance(val, THE_Boolean):
                return THE_Number(1 if val.value else 0)
            
            raise Exception("Can not cast to INT")
        
        if node.name == "FLO":
            if len(node.args) != 1:
                raise Exception("FLo() expects one argument")
            
            val = self.visit(node.args[0])

            if isinstance(val, THE_Number):
                return THE_Number(float(val.value))
            
            if isinstance(val, THE_String):
                return THE_String(float(val.value))     
                    
            raise Exception("Can not cast to FLO")
        
        if node.name == "STR":
            if len(node.args) != 1:
                raise Exception("STR() expects one argument")
            
            val = self.visit(node.args[0])

            try: 
                return THE_String(str(val))

            except:
                raise Exception("Can not cast to STR")
            
        if node.name == "BOOL":
            if len(node.args) != 1:
                raise Exception("BOOL() expects one argument")
            
            val = self.visit(node.args[0])

            if isinstance(val, THE_Number):
                return THE_Boolean(val.value != 0)
            
            if isinstance(val, THE_String):
                return THE_Boolean(len(val.value) > 0)     
                   
            if isinstance(val, THE_Boolean):
                return val
            try:
                return THE_Boolean(True)
            
            except:
                raise Exception("Can not cast to BOOL")

        if node.name == "CHAR":
            if len(node.args) != 1:
                raise Exception("CHAR() expects one argument")
            
            val = self.visit(node.args[0])

            try: 
                return THE_String(chr(val.value))

            except:
                raise Exception("Can not cast to CHAR")
        
        if node.name == "BINT":
            val = self.visit(node.args[0])
            return THE_Number(int(val.value))

        if node.name == "map":
            if len(node.args) != 1:
                raise Exception("array() expects exactly one argument")
            return THE_Map(self.visit(node.args[0]))

        if node.name == "froze_list":
            val = []

            for e in node.args:
                val.append(self.visit(e))
            
            #Need to update after THE_FrozeSet runtime object creation
            return tuple(val)
        
        if node.name == "array":
            if len(node.args) != 1:
                raise Exception("array() expects exactly one argument")
            

            return THE_Array(self.visit(node.args[0]))


        #Builtin-operations OR functions
        if node.name in self.builtin:
            args = [self.visit(arg) for arg in node.args]

            return self.builtin[node.name](args)

        function = None

        for env in reversed(self.env_stack):
            if node.name in env:
                function = env[node.name]
                break

        if function is None:
            raise Exception(f"Undefined function {node.name}")

        new_env = {}

        for i in range(len(function.params)):
            new_env[function.params[i]] = self.visit(node.args[i])

        self.env_stack.append(new_env)

        try:
            for stmt in function.body:
                self.visit(stmt)

        except ReturnSignal as rs:
            self.env_stack.pop()
            return rs.value

        self.env_stack.pop()
        return None

    def visit_MapNode(self, node):
        res = {}

        for key_n, value_n in node.pair:
            key = self.visit(key_n)
            value = self.visit(value_n)

            res[key] = value
        return THE_Map(res)

    def visit_SetNode(self, node):
        values = set()
        for e in node.elements:
            values.add(self.visit(e))

        return THESet(values)

        return values
    def visit_ReturnNode(self, node):
        value = self.visit(node.value)
        raise ReturnSignal(value)
    

    def visit_ArrayNode(self, node):
        values = []

        for e in node.elements:
            values.append(self.visit(e))

        return THE_Array(values)

    def visit_IndexNode(self, node):
        coll = self.visit(node.collection)
        idx = self.visit(node.index)

        return coll.index(idx)

    def visit_FrozeListNode(self, node):
        values = []

        for e in node.elements:
            values.append(self.visit(e))

        return tuple(values)
    
    def visit_StopNode(self, node):
        raise BreakSignal()
    
    def visit_NextNode(self, node):
        raise ContinueSignal()

    def visit_IdleNode(self, node):
        return None
    
    def visit_TryCatchNode(self, node):
        try:
            for try_stmt in node.try_block:
                self.visit(try_stmt)
                
        except Exception as e:
            if not isinstance(e, THEerror):
                e = THEerror(str(e))

            self.last_error = e
            if node.err_var:
                self.env_stack[-1][node.err_var] = str(e)
            for catch_stmt in node.catch_block:
                self.visit(catch_stmt)

    def visit_ThrowNode(self, node):
        val = self.visit(node.value)

        if not isinstance(val, str):
            val = str(val)
        
        raise THEerror(val)


    def visit_RaiseNode(self, node):
        val = self.visit(node.value)

        if not isinstance(val, str):
            raise THEerror(val)
        
        if isinstance(THEerror, val):
            raise val

        raise THEerror(val)

    def run(self, nodes):
        for node in nodes:
            self.visit(node)

        