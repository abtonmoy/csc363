from tokens import *

class TokenStream:
    
    def __init__(self):
        self.tokens: list[Token] = []
        self.pos = 0

    def append(self, token: Token) -> None:
        self.tokens.append(token)

    def __iter__(self):
        return iter(self.tokens)
    
    def __len__(self):
        return len(self.tokens)
    
    def eof(self) -> bool:
        return self.pos >= self.__len__()

    def advance(self):
        if not self.eof():
            self.pos += 1

    def read(self) -> Token:
        if not self.eof():
            tok = self.tokens[self.pos]
            self.advance()
            return tok
        else:
            return Token(TokenType.EOF, '')
    
    def peek(self) -> Token:
        if not self.eof():
            return self.tokens[self.pos]
        else: 
            return Token(TokenType.EOF, '')
