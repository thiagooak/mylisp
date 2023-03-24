import re
import sys
import readline
import os.path as path
import atexit
import sym
import values

def read_history():
    if path.isfile('.tlisp.history'):
        readline.read_history_file('.tlisp.history')


def write_history():
    readline.write_history_file('.tlisp.history')


class Reader:
    def __init__(self):
        self.buffer = ''
        self.pushed = None

    def read_signed(self, sign):
        factor = 1
        if sign == '-':
            factor = -1
        ch = self.getc()
        if ch.isdigit():
            n = self.read_number(ch)
            return factor * n
        self.getc(ch)
        return self.read_sym(sign)

    def read_number(self, digit):
        s = digit
        ch = self.getc()
        while ch and ch.isdigit():
            s += ch
            ch = self.getc()
        self.getc(ch)
        return int(s)

    def read_sym(self, ch):
        result = ch
        ch = self.getc()
        while ch:
            if ch in "()[]\n\t ":
                break
            result += ch
            ch = self.getc()
        self.getc(ch)
        return sym.Symbol(result)

    def read_string(self, ch):
        result = ''
        ch = self.getc()
        while ch and (ch != '"'):
            result += ch
            ch = self.getc()
        return result

    def skip_ws(self):
        ch = self.getc()
        while ch and ch.isspace():
            ch = self.getc()
        self.getc(ch)

    def read_collection(self, end_ch, result_class):
        result = []
        self.skip_ws()
        ch = self.getc()
        while ch and (ch != end_ch):
            self.getc(ch)
            value = self.read_value()
            result.append(value)
            self.skip_ws()
            ch = self.getc()
        return result_class(result)

    def read_value(self):
        result = None
        self.skip_ws()
        ch = self.getc()

        if ch == None:
            return None

        if ch in ['+', '-']:
            return self.read_signed(ch)

        if re.fullmatch(r'[0-9-]', ch):
            return self.read_number(ch)

        if ch == '(':
            return self.read_collection(')', list)

        if ch == '[':
            return self.read_collection(']', values.Vector)

        if ch == "'":
            return [sym.SymQuote, self.read_value()]

        if ch == '"':
            return self.read_string(ch)

        return self.read_sym(ch)


class ConsoleReader(Reader):
    def read_history():
        print("reading history")
        if path.isfile('.tlisp.history'):
            readline.read_history_file('.tlisp.history')

    def write_history():
        print("writing history")
        readline.write_history_file('.tlisp.history')

    def init_history(env):
        read_history()
        atexit.register(write_history)

    def __init__(self, prompt='>> '):
        super().__init__()
        self.prompt = prompt

    def getc(self, ch=None):
        if (ch):
            self.pushed = ch
            return None

        if self.pushed:
            result = self.pushed
            self.pushed = None
            return result

        while len(self.buffer) < 1:
            self.buffer = input(self.prompt)
            self.buffer += "\n"

        result = self.buffer[0]
        self.buffer = self.buffer[1:]
        return result


class FileReader(Reader):
    def __init__(self, path):
        super().__init__()
        self.f = open(path)

    def getc(self, ch=None):
        if (ch):
            self.pushed = ch
            return None

        if self.pushed:
            result = self.pushed
            self.pushed = None
            return result

        while len(self.buffer) < 1:
            self.buffer = self.f.readline()
            if self.buffer == '':
                return None

        result = self.buffer[0]
        self.buffer = self.buffer[1:]
        return result
