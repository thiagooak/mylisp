from charstream import CharStream

class FileCharStream(CharStream):
    def __init__(self, path: str) -> None:
        with open(path) as f:
            text = f.read()
            super().__init__(text)