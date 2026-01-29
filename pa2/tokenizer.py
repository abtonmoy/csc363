from charstream import CharStream
from tokens import Token, TokenType
from tokenstream import TokenStream
import string

RESERVED = {'i', 'f', 'o', 'n', 'p'}
VALID_VARS = set(string.ascii_lowercase) - RESERVED

class Tokenizer:

    def __init__(self, cs: CharStream):
        self.cs = cs
        self.line = 1
        self.column = 0

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
        self.column += 1

        while char in {' ', '\n', '\r', '\t'}:
            if char == '\n':
                self.line += 1
                self.column = 0
            char = self.cs.read()
            self.column += 1
        
        
        if char == '':
            return Token(TokenType.EOF, lexeme = f"{char}")

        # Track position before token
        start_line = self.line
        start_column = self.column

        match char:

            case '=':
                return Token(TokenType.ASSIGN, lexeme = f"{char}")
            
            case '(':
                return Token(TokenType.LPAREN, lexeme = f"{char}")
                
            case ')': 
                return Token(TokenType.RPAREN, lexeme = f"{char}")
            
            case '+':
                return Token(TokenType.PLUS, lexeme = f"{char}")
            
            case '-':
                return Token(TokenType.MINUS, lexeme = f"{char}")
            
            case '*':
                return Token(TokenType.TIMES, lexeme = f"{char}")
            
            case '/':
                return Token(TokenType.DIVIDE, lexeme = f"{char}")
            
            case '^':
                return Token(TokenType.EXPONENT, lexeme = f"{char}")
            
            case 'i':
                return Token(TokenType.INTDEC, lexeme = f"{char}")
            
            case 'p':
                return Token(TokenType.PRINT, lexeme = f"{char}")
            
            case _:
                pass # Move on to secondary inspection to handle digits, vars, error case

        if char.isdigit():
            return self.readintliteral(char, start_line, start_column)


        if char.isalpha():
            if char not in VALID_VARS:
                raise ValueError(f"Invalid variable character: {char} at line {start_line}, column {start_column}")
            else:
                return self.readvariable(char, start_line, start_column)
           
        raise ValueError(f"Unexpected character: {char!r} at line {start_line}, column {start_column}")

    def readintliteral(self, firstchar: str, line: int, column: int) -> Token:
        digits: list[str] = []
        digits.append(firstchar)
        
        # Handle leading zero validation (only allow single '0', not multi-digit with leading zero)
        if firstchar == '0' and not self.cs.eof() and self.cs.peek().isdigit():
            raise ValueError(f"Integer literal cannot have leading zeros at line {line}, column {column}")

        # Read all consecutive digits
        while not self.cs.eof() and self.cs.peek().isdigit():
            digits.append(self.cs.read())
            self.column += 1

        lexeme = ''.join(digits)
        intvalue = int(lexeme)

        return Token(TokenType.INTLIT, lexeme=lexeme, intvalue=intvalue)
    
    def readvariable(self, firstchar: str, line: int, column: int) -> Token:
        chars: list[str] = []
        chars.append(firstchar)
        
        # Read all consecutive valid variable characters
        while not self.cs.eof() and self.cs.peek() in VALID_VARS:
            chars.append(self.cs.read())
            self.column += 1

        lexeme = ''.join(chars)
        
        return Token(TokenType.VARREF, lexeme=lexeme, name=lexeme)
