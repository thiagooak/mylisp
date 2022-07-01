import sys
import re
import readline

class Symbol:
  Symbols = {}

  def intern(name):
    if name in Symbol.Symbols:
      return Symbol.Symbols[name]
    result = Symbol(name)
    Symbol.Symbols[name] = result
    return result

  def __init__(self, s):
    self.name = s

  def __str__(self):
    return f'Symbol #{self.name}'

  def __repr__(self):
    return f'#{self.name}'

  def __hash__(self):
    return hash(self.name)

  def __eq__(self, other):
    return (type(self) == type(other)) and (self.name == other.name)

SymFn = Symbol.intern('fn')
SymDef = Symbol.intern('def')

class SymbolNotFoundError(Exception):
  def __init__(self, symbol, message=None):
    if message:
      self.message = message
    else:
      self.message = f'Symbol not found {symbol}'

    self.symbol = symbol
    super().__init__(self.message)

class Quote:
  def __init__(self, v):
    self.value = v

class ConsoleReader:
  def __init__(self):
    self.buffer = ''
    self.pushed = None

  def getc(self, ch=None):
    if(ch):
      self.pushed = ch
      return None

    if self.pushed:
      result = self.pushed
      self.pushed = None
      return result

    while len(self.buffer) < 1:
      self.buffer = input('>> ')
      if self.buffer == '':
        return None
      self.buffer += "\n"

    result = self.buffer[0]
    self.buffer = self.buffer[1:]
    return result

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
    return Quote(read_value(getc))

  if ch == '"':
    return read_string(getc, ch)

  return read_sym(getc, ch)

def repl(env, reader):
  while True:
    x = read_value(reader.getc)
    if x == None:
      break
    print(eval_value(x, env))

def add(*args):
  result = 0

  if not args:
    return result

  for n in args:
      result += n

  return result

def eval_value(v, env):
  t = type(v)

  if t == int:
    return v

  if t == str:
    return v

  if t == Symbol:
    if v in env:
      return env[v]
    return SymbolNotFoundError(v)

  if t == list:
    if v[0] == SymDef:
      if len(v) != 3:
        raise Exception(f'Wrong number of args ({len(v)}) passed to: def')
      name = v[1]
      value = v[2]
      env[name] = value
      return value

    resolved = list(map(lambda p :  eval_value(p, env), v))

    function = resolved[0]
    params = resolved[1:]

    return function(*params)

  # TBD Add evaluation of strings, symbols, lists, quoted values!

  raise Exception(f'Dont know how to evaluate {v}({t})')

# main program
Env = {Symbol.intern('version'): 100, Symbol.intern('add'): add}
cr  = ConsoleReader()

print(f'MyLISP: I know how to evaluate ints but nothing else.')
print(f'MyLISP: Make me smarter!')
repl(Env, cr)
