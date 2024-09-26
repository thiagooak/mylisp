from symbol import Symbol
from list import List, to_lisp_list
from streams import EOF, ConsoleCharStream
import re

LEFT_PAREN_SYM = Symbol('(')
RIGHT_PAREN_SYM = Symbol(')')
NONE_SYM = Symbol('None')
TRUE_SYM = Symbol('True')
FALSE_SYM = Symbol('False')

def skip_comment(ch_stream) -> None:
    # Skip the semicolon.
    ch_stream.read()

    # Loop until we see the end of line or EOF.
    ch = ch_stream.read()
    while ch != EOF:
        if ch in "\n\r":
            break
        ch = ch_stream.read()

def skip_ws(ch_stream) -> None:
    ch = ch_stream.peek()
    while ch != EOF:
        if ch.isspace():
            ch_stream.read()
            ch = ch_stream.peek()
        elif ch == ';':
            skip_comment(ch_stream)
            ch = ch_stream.peek()
        else:
            break

def read_string(ch_stream):
    # Ignore the leading quote.
    ch_stream.read()

    # Loop until we see another quote.
    value = ''
    ch = ch_stream.read()
    while (ch != EOF) and (ch != "'"):
        value += ch
        ch = ch_stream.read()

    # EOF in the middle of a string?
    if ch == EOF:
        raise Exception('End of file while reading string.')

    return value

def read_token(ch_stream) -> str:
    token = ch_stream.read()
    ch = ch_stream.peek()
    while ch != EOF:
        if (ch in '()') or ch.isspace():
            break
        token += ch_stream.read()
        ch = ch_stream.peek()
    return token

def read_number_or_symbol(ch_stream) -> int|float|Symbol:
    token = read_token(ch_stream)
    if re.match(r'[+-]?\d+\.\d', token):
        return float(token)
    elif re.match(r'[+-]?\d+', token):
        return int(token)
    else:
        return Symbol(token)

def read_simple_value(ch_stream) -> object:
    skip_ws(ch_stream)
    ch = ch_stream.peek()
    if ch == EOF:
        value = EOF
    elif ch == "'":
        value = read_string(ch_stream)
    elif ch in '()':
        value = Symbol(ch_stream.read())
    else:
        value = read_number_or_symbol(ch_stream)
    return value

def read_list(ch_stream) -> List:
    result = []
    value = read_value(ch_stream)
    while value != RIGHT_PAREN_SYM and value != EOF:
        result.append(value)
        value = read_value(ch_stream)

    if value == EOF:
        raise Exception('End of file while reading a list.')

    return to_lisp_list(result)

def read_value(ch_stream) -> object:
    value = read_simple_value(ch_stream)

    if value == NONE_SYM:
        value = None
    elif value == TRUE_SYM:
        value = True
    elif value == FALSE_SYM:
        value = False
    elif value == LEFT_PAREN_SYM:
        value = read_list(ch_stream)

    return value