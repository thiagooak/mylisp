
import re
from sym import Symbol

SymQuote = Symbol.intern('quote')


class Reader:
    def getc(self, ch=None):
        if (ch):
            self.pushed = ch
            return None

        if self.pushed:
            result = self.pushed
            self.pushed = None
            return result

        while len(self.buffer) < 1:
            self.buffer = self.read_line()
            if self.buffer == '':
                return None
            self.buffer += "\n"

        result = self.buffer[0]
        self.buffer = self.buffer[1:]
        return result


class FileReader(Reader):
    def __init__(self, path):
        self.buffer = ''
        self.pushed = None
        self.f = open(path)

    def read_line(self):
        return self.f.readline()


class ConsoleReader(Reader):
    def __init__(self, prompt='>> '):
        self.buffer = ''
        self.pushed = None
        self.prompt = prompt

    def read_line(self):
        return input(self.prompt)


def read_number(getc, digit):
    s = digit
    ch = getc()
    while ch and ch.isdigit():
        s += ch
        ch = getc()
    getc(ch)
    return int(s)


def read_sym(getc, ch):
    result = ch
    ch = getc()
    while ch and (not ch.isspace()):
        if ch == '(' or ch == ')' or ch == "\n":
            break
        result += ch
        ch = getc()
    getc(ch)
    return Symbol(result)


def read_string(getc, ch):
    result = ''
    ch = getc()
    while ch and (ch != '"'):
        result += ch
        ch = getc()
    return result


def read_list(getc, ch):
    result = []
    ch = getc()
    while ch and (ch != ')'):
        getc(ch)
        value = read_value(getc)
        result.append(value)
        ch = getc()
    return result


def read_value(getc):
    result = None

    ch = getc()
    while ch and ch.isspace():
        ch = getc()

    if ch == None:
        return ch

    if re.fullmatch(r'[0-9+-]', ch):
        return read_number(getc, ch)

    if ch == '(':
        return read_list(getc, ch)

    if ch == "'":
        return [SymQuote, read_value(getc)]

    if ch == '"':
        return read_string(getc, ch)

    return read_sym(getc, ch)
