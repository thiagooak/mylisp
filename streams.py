from symbol import Symbol

# Make up a special value to indicate the end of file.
EOF = Symbol('* EOF *')

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


class ConsoleCharStream(CharStream):
    def __init__(self, prompt='mylisp> '):
        super().__init__('')
        self.prompt = prompt

    def peek(self):
        if self.position < 0:
            return EOF
        if self.position >= len(self.text):
            try:
                self.text = input(self.prompt)
                self.text += '\n'
                self.position = 0
            except KeyboardInterrupt or EOFError: # @BOOK I get KeyboardInterrupt a lot
                self.position = -1
                return EOF

        return self.text[self.position]


class FileCharStream(CharStream):
    def __init__(self, path: str) -> None:
        with open(path) as f:
            text = f.read()
            super().__init__(text)
