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
        varname = statement.varname
        if varname in declared:
            raise SemanticError(f"Variable {varname!r} redeclared at line {linenumber}")
        declared.append(varname)
        return

    if isinstance(statement, PrintNode):
        varname = statement.varname
        if varname not in declared:
            raise SemanticError(f"Trying to print undeclared variable {varname!r} at line {linenumber}")
        if varname not in initialized:
            raise SemanticError(f"Trying to print uninitialized variable {varname!r} at line {linenumber}")
        return

    if isinstance(statement, AssignNode):
        varname = statement.varname
        if varname not in declared:
            raise SemanticError(f"Assignment to undeclared variable {varname!r} at line {linenumber}")
        _semantic_check_expr(statement.expr, declared, initialized, linenumber)
        if varname not in initialized:
            initialized.append(varname)
        return

    raise SemanticError(f"Unknown statement type at line {linenumber}")
    # Catches any weird statement types; this should never happen for a validly parsed program
    # Keeping it here though will help if your parser has an undiscovered or unfixed bug


def _semantic_check_expr(expr: ASTNode, declared: list[str], initialized: list[str], linenumber: int):
    if isinstance(expr, IntLitNode):
        return
    
    if isinstance(expr, VarRefNode):
        varname = expr.varname
        if varname not in declared:
            raise SemanticError(f"Use of undeclared variable {varname!r} at line {linenumber}")
        if varname not in initialized:
            raise SemanticError(f"Use of unitialized variable {varname!r} at line {linenumber}")
        return

    if isinstance(expr, BinOpNode):
        _semantic_check_expr(expr.left, declared, initialized, linenumber)
        _semantic_check_expr(expr.right, declared, initialized, linenumber)
        return
    
    raise SemanticError(f"Unknown expression type at line {linenumber}")
    # Catches any weird statement types; this should never happen for a validly parsed program
    # Keeping it here though will help if your parser has an undiscovered or unfixed bug