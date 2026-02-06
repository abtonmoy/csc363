from tokens import TokenType



class ASTNode:
    def __init__(self):
        pass
    

class IntDclNode(ASTNode):
    def __init__(self, varname:str):
        self.varname = varname

    def __repr__(self):
        return f"[IntDclNode varname={self.varname!r}]"
    

class PrintNode(ASTNode):
    def __init__(self, varname:str):
        self.varname = varname
    def __repr__(self):
        return f"[PrintNode varname={self.varname!r}]"


class VarRefNode(ASTNode):
    def __init__(self, varname:str):
        self.varname = varname
    def __repr__(self):
        return f"[VarRefNode varname={self.varname!r}]"


class IntLitNode(ASTNode):
    def __init__(self, value:int):
        self.value = value
    def __repr__(self):
        return f"[IntLitNode value={self.value!r}]"


class AssignNode(ASTNode):
    def __init__(self, varname:str, expr):
        self.varname = varname
        self.expr = expr

    def __repr__(self):
        return f"[AssignNode varname={self.varname!r} expr={self.expr!r}]"


class BinOpNode(ASTNode):
    def __init__(self, optype: TokenType, left, right):
        self.optype = optype
        self.left = left
        self.right = right

    def __repr__(self):
        return f"[BinOpNode optype={self.optype} left={self.left!r} right={self.right!r}]"
