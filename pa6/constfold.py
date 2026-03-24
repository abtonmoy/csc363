from acdcast import *
from tokens import TokenType


def constant_fold(program: list[ASTNode]) -> list[ASTNode]:
    """Apply constant folding optimization to every statement in the program."""
    folded = []
    for stmt in program:
        folded.append(_fold_stmt(stmt))
    return folded


def _fold_stmt(stmt: ASTNode) -> ASTNode:
    """Fold constant sub-expressions within a single statement."""

    if isinstance(stmt, AssignNode):
        folded_expr = _fold_expr(stmt.expr)
        return AssignNode(stmt.varname, folded_expr)

    # IntDclNode, PrintNode — nothing to fold
    return stmt


def _fold_expr(expr: ASTNode) -> ASTNode:
    """Recursively fold constant sub-expressions bottom-up."""

    if isinstance(expr, IntLitNode):
        return expr

    if isinstance(expr, VarRefNode):
        return expr

    if isinstance(expr, BinOpNode):
        left = _fold_expr(expr.left)
        right = _fold_expr(expr.right)

        # Both children are literals — evaluate at compile time
        if isinstance(left, IntLitNode) and isinstance(right, IntLitNode):
            result = _evaluate(expr.optype, left.value, right.value)
            if result is not None:
                return IntLitNode(result)

        # At least one child is not a literal — return partially folded node
        return BinOpNode(expr.optype, left, right)

    # Fallback (should not happen for a valid AST)
    return expr


def _evaluate(optype: TokenType, left: int, right: int):
    """Evaluate a binary operation on two integer values.
    
    Returns the integer result, or None if the operation cannot be folded
    (e.g. division by zero).
    """
    if optype == TokenType.PLUS:
        return left + right
    elif optype == TokenType.MINUS:
        return left - right
    elif optype == TokenType.TIMES:
        return left * right
    elif optype == TokenType.DIVIDE:
        if right == 0:
            return None  # Don't fold division by zero; let dc handle it
        return int(left / right)
    elif optype == TokenType.EXPONENT:
        return left ** right

    return None
