from charstream import CharStream
from tokens import Token, TokenType
from tokenstream import TokenStream
import string

RESERVED = {'i', 'f', 'o', 'n', 'p', 'l', 's'}
VALID_VARS = set(string.ascii_lowercase) - RESERVED

class Tokenizer:

    def __init__(self, cs: CharStream):
        self.cs = cs
        # added: line and column tracking for error messages
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
        # added: column tracking
        self.column += 1

        while char in {' ', '\n', '\r', '\t'}:
            # added: line tracking for newlines
            if char == '\n':
                self.line += 1
                self.column = 0
            char = self.cs.read()
            self.column += 1
        
        
        if char == '':
            return Token(TokenType.EOF, lexeme = f"{char}")

        # added: track token position for error messages
        start_line = self.line
        start_column = self.column

        match char:

            case '=':
                return Token(TokenType.ASSIGN, lexeme = f"{char}")
            
            case '(':
                # modified: replaced NotImplementedError
                return Token(TokenType.LPAREN, lexeme = f"{char}")
                
            case ')': 
                # modified: replaced NotImplementedError
                return Token(TokenType.RPAREN, lexeme = f"{char}")
            
            case '+':
                # modified: replaced NotImplementedError
                return Token(TokenType.PLUS, lexeme = f"{char}")
            
            case '-':
                # modified: replaced NotImplementedError
                return Token(TokenType.MINUS, lexeme = f"{char}")
            
            case '*':
                # modified: replaced NotImplementedError
                return Token(TokenType.TIMES, lexeme = f"{char}")
            
            case '/':
                # modified: replaced NotImplementedError
                return Token(TokenType.DIVIDE, lexeme = f"{char}")
            
            case '^':
                # modified: replaced NotImplementedError
                return Token(TokenType.EXPONENT, lexeme = f"{char}")
            
            case 'i':
                # modified: replaced NotImplementedError
                return Token(TokenType.INTDEC, lexeme = f"{char}")
            
            case 'p':
                # modified: replaced NotImplementedError
                return Token(TokenType.PRINT, lexeme = f"{char}")
            
            case _:
                pass # Move on to secondary inspection to handle digits, vars, error case

        if char.isdigit():
            # modified: changed to return directly from method with position params
            return self.readintliteral(char, start_line, start_column)


        if char.isalpha():
            if char not in VALID_VARS:
                # modified: added position to error message
                raise ValueError(f"Invalid variable character: {char} at line {start_line}, column {start_column}")
            else:
                # modified: replaced NotImplementedError with method call
                return self.readvariable(char, start_line, start_column)
            
        # modified: added position to error message
        raise ValueError(f"Unexpected character: {char!r} at line {start_line}, column {start_column}")

    # modified: updated signature and implementation
    def readintliteral(self, firstchar: str, line: int, column: int) -> Token:
        digits: list[str] = []
        digits.append(firstchar)
        
        # added: leading zero validation
        if firstchar == '0' and not self.cs.eof() and self.cs.peek().isdigit():
            raise ValueError(f"Integer literal cannot have leading zeros at line {line}, column {column}")

        # added: read all consecutive digits
        while not self.cs.eof() and self.cs.peek().isdigit():
            digits.append(self.cs.read())
            self.column += 1

        lexeme = ''.join(digits)
        intvalue = int(lexeme)

        return Token(TokenType.INTLIT, lexeme=lexeme, intvalue=intvalue)
    
    # added: new method for variable parsing
    def readvariable(self, firstchar: str, line: int, column: int) -> Token:
        chars: list[str] = []
        chars.append(firstchar)
        
        # Read all consecutive valid variable characters
        while not self.cs.eof() and self.cs.peek() in VALID_VARS:
            chars.append(self.cs.read())
            self.column += 1

        lexeme = ''.join(chars)
        
        return Token(TokenType.VARREF, lexeme=lexeme, name=lexeme)
