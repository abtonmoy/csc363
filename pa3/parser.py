from tokens import Token, TokenType
from tokenstream import *
from acdcast import *

class ParseError(Exception):
    pass 


def parse(ts: TokenStream) -> ASTNode:
    """Parse a single statement from the token stream.

    Policy: each TokenStream represents exactly one line/statement.
    Therefore, after parsing a statement we must be at EOF.
    """
    t = ts.peek()
    #print(f"parse() peeked: {t}")

    if t.tokentype == TokenType.PRINT:
        ts.read()
        if t.name is None:
            raise ParseError("Malformed PRINT token")
        node = PrintNode(t.name)
        expect(ts, TokenType.EOF)
        return node

    if t.tokentype == TokenType.INTDEC:
        ts.read()
        if t.name is None:
            raise ParseError("Malformed INTDEC token")
        node = IntDclNode(t.name)
        expect(ts, TokenType.EOF)
        return node

    if t.tokentype == TokenType.VARREF:
        lhs = ts.read()
        expect(ts, TokenType.ASSIGN)
        rhs = parse_expression(ts)
        if lhs.lexeme is None:
            raise ParseError("Malformed VARREF token on LHS")
        node = AssignNode(lhs.lexeme, rhs)
        expect(ts, TokenType.EOF)
        return node

    raise ParseError(
        f"Expected TokenType.PRINT, TokenType.INTDCL/INTDEC, or TokenType.VARREF; got {t.tokentype}"
    )


def parse_expression(ts: TokenStream) -> ASTNode:
    """Parse an infix arithmetic expression using shunting-yard, producing an AST."""

    opstack = []   
    valstack = []

    precedence = {
        TokenType.EXPONENT: 3,
        TokenType.TIMES: 2,
        TokenType.DIVIDE: 2,
        TokenType.PLUS: 1,
        TokenType.MINUS: 1,
    }

    # True means left-associative
    leftassoc = {
        TokenType.EXPONENT: False,
        TokenType.TIMES: True,
        TokenType.DIVIDE: True,
        TokenType.PLUS: True,
        TokenType.MINUS: True,
    }

    operatortypes = {
        TokenType.PLUS,
        TokenType.MINUS,
        TokenType.TIMES,
        TokenType.DIVIDE,
        TokenType.EXPONENT,
    }
    
    valid_followers = {TokenType.INTLIT, TokenType.VARREF, TokenType.LPAREN}

    while ts.peek().tokentype != TokenType.EOF:
        tok = ts.peek()

        if tok.tokentype == TokenType.INTLIT:
            tok = ts.read()
            if tok.intvalue is None:
                raise ParseError("Malformed INTLIT token")
            next_tok = ts.peek()
            if (next_tok.tokentype in operatortypes) or (next_tok.tokentype == TokenType.RPAREN) or (next_tok.tokentype == TokenType.EOF):
                valstack.append(IntLitNode(tok.intvalue))
                continue
            raise ParseError("Expected operator or rparen after int literal")

        if tok.tokentype == TokenType.VARREF:
            tok = ts.read()
            if tok.name is None:
                raise ParseError("Malformed VARREF token")
            next_tok = ts.peek()
            if (next_tok.tokentype in operatortypes) or (next_tok.tokentype == TokenType.RPAREN) or (next_tok.tokentype == TokenType.EOF):
                valstack.append(VarRefNode(tok.name))
                continue
            raise ParseError("Expected operator or rparen after variable")

        if tok.tokentype == TokenType.LPAREN:
            ts.read()
            next_tok = ts.peek()
            if next_tok.tokentype not in valid_followers:
                raise ParseError("Expected lparen, intlit, or varref after lparen")
            opstack.append(tok)
            continue

        if tok.tokentype == TokenType.RPAREN:
            ts.read()
            found_lparen = False
            while len(opstack) > 0:
                top = opstack[-1]
                if top.tokentype == TokenType.LPAREN:
                    opstack.pop()
                    found_lparen = True
                    break
                reduce(opstack, valstack)
            
            if not found_lparen:
                 raise ParseError("Mismatched parentheses")
            continue

        if tok.tokentype in operatortypes:
            incoming = ts.read()
            
            next_tok = ts.peek()
            if next_tok.tokentype not in valid_followers:
                 raise ParseError("Expected operand or lparen after operator")

            while len(opstack) > 0 and opstack[-1].tokentype in operatortypes:
                top = opstack[-1]

                top_prec = precedence[top.tokentype]
                inc_prec = precedence[incoming.tokentype]

                is_left = leftassoc[incoming.tokentype]
                if (is_left and top_prec >= inc_prec) or (not is_left and top_prec > inc_prec):
                     reduce(opstack, valstack)
                else:
                    break

            opstack.append(incoming)
            continue

        raise ParseError(f"Unexpected token in expression: {tok}")

    while len(opstack) > 0:
        top = opstack[-1]
        if top.tokentype == TokenType.LPAREN:
            raise ParseError("Mismatched parentheses")
        
        reduce(opstack, valstack)

    if len(valstack) != 1:
        raise ParseError("Expression did not reduce to one AST")

    return valstack.pop()


def reduce(opstack: list, valstack: list) -> None:
    """Pop one operator and two operands to build a BinOpNode and push it back."""
    if len(opstack) < 1:
        raise ParseError("Internal error: reduce called with empty opstack")
    
    op_token = opstack.pop()
    
    if len(valstack) < 2:
        raise ParseError(f"Expected two operands for operator {op_token.tokentype}")

    right = valstack.pop()
    left = valstack.pop()

    node = BinOpNode(op_token.tokentype, left, right)
    valstack.append(node)


def expect(ts: TokenStream, expectedtype: TokenType) -> Token:
    tok = ts.peek()
    if tok.tokentype == expectedtype:
        return ts.read()
    
    raise ParseError(f"Expected {expectedtype} but found {tok.tokentype}")
