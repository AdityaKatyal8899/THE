class ASTNode:
    pass

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value
       
class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value
    

class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name


class BooleanNode(ASTNode):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f"{self.value}"

class AssignNode(ASTNode):
    def __init__(self, identifier,value):
        self.identifier = identifier
        self.value = value

class GiveNode(ASTNode):
    def __init__(self, value, start, end):
        self.value = value
        self.start = start
        self.end = end
   
class BinaryOpNode(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class UnaryOpNode(ASTNode):
    def __init__(self, value, operand):
        self.value = value
        self.operand = operand
    
class IfElseNode(ASTNode):
    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block


class LoopTillNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class LoopInNode(ASTNode):
    def __init__(self, it, var, body):
        self.it = it
        self.var = var
        self.body = body

class GetNode(ASTNode):
    def __init__(self, prompt):
        self.prompt = prompt

class CallNode(ASTNode):
    def __init__(self, name, args):
        self.name = name 
        self.args = args

class FunctionNode(ASTNode):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class ReturnNode(ASTNode):
    def __init__(self, value):
        self.value = value

class ArrayNode(ASTNode):
    def __init__(self, elements):
        self.elements = elements

class IndexNode(ASTNode):
    def __init__(self, collection, index):
        self.collection = collection
        self.index = index        

class FrozeListNode(ASTNode):
    def __init__(self, elements):
        self.elements = elements

class MapNode(ASTNode):
    def __init__(self, pairs):
        self.pair = pairs

class SetNode(ASTNode):
    def __init__(self, elements):
        self.elements = elements

class MethodCallNode(ASTNode):
    def __init__(self, object, method, args):
        self.object = object
        self.method = method
        self.args = args

class TryCatchNode(ASTNode):
    def __init__(self, try_block, catch_block, err_var=None):
        self.try_block = try_block
        self.catch_block = catch_block
        self.err_var = err_var


class ThrowNode(ASTNode):
    def __init__(self, value):
        self.value = value


class RaiseNode(ASTNode):
    def __init__(self, value):
        self.value = value

class StopNode(ASTNode):
    pass

class NextNode(ASTNode):
    pass
class IdleNode(ASTNode):
    pass
