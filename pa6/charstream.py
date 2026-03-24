# EOF is signaled by ''
# pos is the position of the next character to be consumed
# so advance() moves the read head forward but does not consume a char
# peek reads the char at the read head but does not advance the read head
# read reads the char at the read head and advances the read head
# exception: EOF
class CharStream:
    def __init__(self, source:str):
        self.source = source
        self.pos = 0
        self.sourcelen = len(source)

    def eof(self) -> bool:
        return self.pos >= self.sourcelen

    def peek(self) -> str: 
        # Really returns only a char
        # If EOF, returns empty string ''
        if self.eof():
            return ''
        else:
            return self.source[self.pos]
    
    def advance(self) -> None:
        # If EOF, does nothing
        # Otherwise, increments pos
        if not self.eof():
            self.pos += 1

    def read(self) -> str:
        # Really returns only a char
        # If EOF, returns empty string ''
        if self.eof():
            return ''
        else:        
            c = self.source[self.pos]
            self.advance()
            return c
