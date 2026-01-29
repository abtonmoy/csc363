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
                raise NotImplementedError
                
            case ')': 
                raise NotImplementedError
            
            case '+':
                raise NotImplementedError
            
            case '-':
                raise NotImplementedError
            
            case '*':
                raise NotImplementedError
            
            case '/':
                raise NotImplementedError
            
            case '^':
                raise NotImplementedError
            
            case 'i':
                raise NotImplementedError

            case 'p':
                raise NotImplementedError
            
            case _:
                pass # Move on to secondary inspection to handle digits, vars, error case

        if char.isdigit():
            lexeme, intvalue = self.readintliteral(char)
            return Token(TokenType.INTLIT, lexeme = lexeme, intvalue = intvalue)


        if char.isalpha():
            if char not in VALID_VARS:
                raise ValueError(f"Invalid variable character: {char}")
            else:
                raise NotImplementedError
           
        raise ValueError(f"Unexpected character: {char!r}")
        
    

    def readintliteral(self, firstchar: str) -> tuple[str, int]:
        
        digits: list[str] = []
        digits.append(firstchar)
        #if CONDITION:
        #    raise ValueError("Integer literal cannot have a leading zero")

        #while not self.cs.eof() and SOMETHING:
        #    digits.append(SOMETHING)

        lexeme = ''.join(digits)

        return lexeme, int(lexeme)
