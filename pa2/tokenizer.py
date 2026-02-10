from charstream import CharStream
from tokens import Token, TokenType
from tokenstream import TokenStream
import string

RESERVED = {'i', 'f', 'o', 'n', 'p', 'l', 's'}
VALID_VARS = set(string.ascii_lowercase) - RESERVED

class Tokenizer:

    def __init__(self, cs: CharStream):
        self.cs = cs

    def tokenize(self) -> TokenStream:
        ts = TokenStream()
        while True:
            tok = self.nexttoken()
            ts.append(tok)
            if tok.tokentype == TokenType.EOF:
                break

        return ts
    

    def nexttoken(self) -> Token:

        char = self.cs.read()

        while char in {' ', '\n', '\r', '\t'}:
            char = self.cs.read() # Consume chars for space, newline, etc.
        
        
        if char == '':
            return Token(TokenType.EOF, lexeme = f"{char}")



        match char:

            case '=':
                return Token(TokenType.ASSIGN, lexeme = f"{char}")
            
            case '(':
                return Token(TokenType.LPAREN, lexeme=char)
            case ')':
                return Token(TokenType.RPAREN, lexeme=char)
            case '+':
                return Token(TokenType.PLUS, lexeme=char)
            case '-':
                return Token(TokenType.MINUS, lexeme=char)
            case '*':
                return Token(TokenType.TIMES, lexeme=char)
            case '/':
                return Token(TokenType.DIVIDE, lexeme=char)
            case '^':
                return Token(TokenType.EXPONENT, lexeme=char)
            case 'i':
                nextchar = self.cs.read()
                while nextchar in {' ', '\n', '\r', '\t'}:
                    nextchar = self.cs.read()
                if nextchar not in VALID_VARS:
                    raise ValueError(f"invalid variable character: {nextchar!r}" if nextchar else "Unexpected end of input")
                return Token(TokenType.INTDEC, lexeme=f"i{nextchar}", name=nextchar)
            case 'p':
                nextchar = self.cs.read()
                while nextchar in {' ', '\n', '\r', '\t'}:
                    nextchar = self.cs.read()
                if nextchar not in VALID_VARS:
                    raise ValueError(f"invald variable character: {nextchar!r}" if nextchar else "unexpected end of input")
                return Token(TokenType.PRINT, lexeme=f"p{nextchar}", name=nextchar)
            case _:
                pass

        if char.isdigit():
            lexeme, intvalue = self.readintliteral(char)
            return Token(TokenType.INTLIT, lexeme = lexeme, intvalue = intvalue)


        if char.isalpha():
            if char not in VALID_VARS:
                raise ValueError(f"Invalid variable character: {char}")
            return Token(TokenType.VARREF, lexeme=char)
           
        raise ValueError(f"Unexpected character: {char!r}")
        
    

    def readintliteral(self, firstchar: str) -> tuple[str, int]:
        digits: list[str] = []
        digits.append(firstchar)
        if firstchar == '0' and not self.cs.eof() and self.cs.peek().isdigit():
            raise ValueError("Integer literal cannot have a leading zero")
        while not self.cs.eof() and self.cs.peek().isdigit():
            digits.append(self.cs.read())
        lexeme = ''.join(digits)
        return lexeme, int(lexeme)