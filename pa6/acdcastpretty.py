from acdcast import *


# Pretty-printing is a debugging aid.
# Keep __repr__ in acdcast.py as the canonical, test-friendly representation.


def _label(node: ASTNode) -> str:
    """Return a one-line label for a node."""
    # Statement nodes
    if isinstance(node, AssignNode):
        return f"Assign(varname={node.varname!r})"
    if isinstance(node, PrintNode):
        return f"Print(varname={node.varname!r})"
    if isinstance(node, IntDclNode):
        return f"IntDcl(varname={node.varname!r})"

    # Expression nodes
    if isinstance(node, BinOpNode):
        # If optype is an Enum (e.g., TokenType), prefer its .name.
        op = getattr(node.optype, "name", str(node.optype))
        return f"BinOp(op={op})"
    if isinstance(node, IntLitNode):
        return f"IntLit(value={node.value})"
    if isinstance(node, VarRefNode):
        return f"VarRef(varname={node.varname!r})"

    # Fallback for future extensions
    return type(node).__name__


def _children(node: ASTNode) -> list:
    """Return child nodes in display order."""
    if isinstance(node, AssignNode):
        return [node.expr]
    if isinstance(node, BinOpNode):
        return [node.left, node.right]

    # Leaves / no children
    return []


def _pretty_lines(node: ASTNode, prefix: str = "", is_last: bool = True) -> list:
    """Build lines for a console tree using unicode box-drawing characters."""
    lines = []

    # Root prints without a branch connector.
    if prefix == "" and is_last:
        lines.append(_label(node))
    else:
        connector = "└─ " if is_last else "├─ "
        lines.append(prefix + connector + _label(node))

    kids = _children(node)
    if not kids:
        return lines

    # Extend prefix for children.
    child_prefix = prefix + ("   " if is_last else "│  ")

    for i, child in enumerate(kids):
        child_is_last = (i == len(kids) - 1)
        lines.extend(_pretty_lines(child, child_prefix, child_is_last))

    return lines


def pretty_str(node: ASTNode) -> str:
    """Return a human-friendly, tree-shaped view of the AST."""
    if node is None:
        return "<None>"
    return "\n".join(_pretty_lines(node))


def pretty_print(node: ASTNode) -> None:
    """Print a human-friendly, tree-shaped view of the AST."""
    print(pretty_str(node))