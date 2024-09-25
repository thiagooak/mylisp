from symbol import Symbol

# Make up a special value to indicate the end of file.
EOF = Symbol('* EOF *')

# The base character stream class.
class CharStream:
    def __init__(self, text) -> None:
        self.text = text
        self.position = 0

    def peek(self) -> str | Symbol:
        if self.position >= len(self.text):
            return EOF
        ch = self.text[self.position]
        return ch

    def read(self) -> str | Symbol:
        ch = self.peek()
        self.position += 1
        return ch