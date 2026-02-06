from enum import Enum

class TokenType(Enum):
    PRINT = 0
    INTDEC = 1
    INTLIT = 2
    VARREF = 3
    ASSIGN = 4
    PLUS = 5
    MINUS = 6
    TIMES = 7
    DIVIDE = 8
    EXPONENT = 9
    LPAREN = 10
    RPAREN = 11
    EOF = 12
    EOTS = 13



class Token:

    def __init__(
        self, 
        tokentype: TokenType, 
        lexeme: str,
        *,  
        name: str | None = None,
        intvalue: int | None = None,
    ):

        self.tokentype = tokentype
        self.lexeme = lexeme
        self.name = name
        self.intvalue = intvalue

    def __str__(self):
        namepart = f"; name: {self.name}" if self.name is not None else ""
        intvalpart = f"; intval: {str(self.intvalue)}" if self.intvalue is not None else ""

        return f"[Token type: {self.tokentype}; lexeme: {self.lexeme}{namepart}{intvalpart}]"

    def __repr__(self):
        return self.__str__()
    
