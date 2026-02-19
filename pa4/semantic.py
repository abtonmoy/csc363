from acdcast import *

class SemanticError(Exception):
    pass


def semanticanalysis(program: list[ASTNode]) -> None:

    declared = []
    initialized = []

    for linenumber, statement in enumerate(program, start=1):
        _semantic_check_stmt(statement, declared, initialized, linenumber)
    
    return 


def _semantic_check_stmt(statement: ASTNode, declared: list[str], initialized: list[str], linenumber: int) -> None:

    if isinstance(statement, IntDclNode):
        raise NotImplementedError
        # SemanticError(f"Variable {varname!r} redeclared at line {linenumber}")
        
    
    if isinstance(statement, PrintNode):
        raise NotImplementedError
        # SemanticError(f"Trying to print undeclared variable {varname!r} at line {linenumber}")
        # SemanticError(f"Trying to print uninitialized variable {varname!r} at line {linenumber}")
    
    if isinstance(statement, AssignNode):
        raise NotImplementedError
        # SemanticError(f"Assignment to undeclared variable {varname!r} at line {linenumber}")


    raise SemanticError("Unknown statement type at line {linenumber}")
    # Catches any weird statement types; this should never happen for a validly parsed program
    # Keeping it here though will help if your parser has an undiscovered or unfixed bug


def _semantic_check_expr(expr: ASTNode, declared: list[str], initialized: list[str], linenumber: int):
    if isinstance(expr, IntLitNode):
        return
    
    if isinstance(expr, VarRefNode):
        raise NotImplementedError
        # SemanticError(f"Use of undeclared variable {varname!r} at line {linenumber}")
        # SemanticError(f"Use of unitialized variable {varname!r} at line {linenumber}")
        
    if isinstance(expr, BinOpNode):
        # Two recursive calls go here...
        return
    
    raise SemanticError(f"Unknown expression type at line {linenumber}")
    # Catches any weird statement types; this should never happen for a validly parsed program
    # Keeping it here though will help if your parser has an undiscovered or unfixed bug