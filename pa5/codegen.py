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

        raise NotImplementedError


    if isinstance(statement, IntLitNode):

        raise NotImplementedError


    if isinstance(statement, VarRefNode):

        raise NotImplementedError
    
    if isinstance(statement, PrintNode):

        raise NotImplementedError

    
    if isinstance(statement, AssignNode):

        raise NotImplementedError
    

    if isinstance(statement, BinOpNode):

        raise NotImplementedError
    

    # Should never get here
    return code
