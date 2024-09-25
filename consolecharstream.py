from charstream import CharStream, EOF

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
            except(EOFError):
                self.position = -1
                return EOF

        return self.text[self.position]