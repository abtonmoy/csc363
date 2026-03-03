from acdcast import *

class InstructionList:

    def __init__(self):

        self.instructions = []

    def append(self, instruction: str):

        self.instructions.append(instruction)

    def extend(self, newinstructions: "InstructionList"):
        
        self.instructions.extend(newinstructions.instructions)

    def __iter__(self):
        return iter(self.instructions)




def codegenerator(program: list[ASTNode]) -> InstructionList:

    code = InstructionList()

    for statement in program:

        newcode = stmtcodegen(statement)
        code.extend(newcode)

    return code
    

def stmtcodegen(statement: ASTNode) -> InstructionList:

    code = InstructionList()

    if isinstance(statement, IntDclNode):
        return code


    if isinstance(statement, IntLitNode):
        code.append(str(statement.value))
        return code


    if isinstance(statement, VarRefNode):
        code.append(f"l{statement.varname}")
        return code
    
    if isinstance(statement, PrintNode):
        code.append(f"l{statement.varname}")
        code.append("p")
        return code
    
    
    if isinstance(statement, AssignNode):
        expr_code = stmtcodegen(statement.expr)
        code.extend(expr_code)
        code.append(f"s{statement.varname}")
        return code
    
    
    if isinstance(statement, BinOpNode):
        left_code = stmtcodegen(statement.left)
        right_code = stmtcodegen(statement.right)
        
        code.extend(left_code)
        code.extend(right_code)
        
        if statement.optype == TokenType.PLUS:
            code.append("+")
        elif statement.optype == TokenType.MINUS:
            code.append("-")
        elif statement.optype == TokenType.TIMES:
            code.append("*")
        elif statement.optype == TokenType.DIVIDE:
            code.append("/")
        elif statement.optype == TokenType.EXPONENT:
            code.append("^")
        
        return code
    
    # Should never get here
    return code
