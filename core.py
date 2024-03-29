import sym
import eval as e
import reader as r


def tron(env):
    env[sym.SymTrace] = True

def troff(env):
    env[sym.SymTrace] = False

def to_string(v):
    t = type(v)

    if t == int:
        return str(v)

    if t == str:
        return '"' + v + '"'

    if t == sym.Symbol:
        return v.name

    if t == list:
        result = []
        for i in v:
            result.append(to_string(i))
        return '(' + ' '.join(result) + ')'

    return str(v)


def source(env, path):
    reader = r.FileReader(path)
    repl(env, reader, False)


def read(env):
    reader = r.ConsoleReader(prompt='> ')
    while True:
        x = reader.read_value()
        if x == None:
            break
        return x


def print_me(env, v):
    print(to_string(v))


def if_me(env, test, then, otherwise=None):
    if e.eval_value(env, test):
        return e.eval_value(env, then)

    if otherwise:
        return e.eval_value(env, otherwise)

    return None


def loop(env, v):
    while True:
        (e.eval_value(env, v))


def repl(env, reader, print_result=True):
    while True:
        x = reader.read_value()
        if x == None:
            break
        result = e.eval_value(env, x)
        if print_result:
            print(to_string(result))


def implicit_do(env, exprs):
    result = None
    for i in range(len(exprs)):
        result = e.eval_value(env, exprs[i])
    return result


def add(env, *args):
    result = 0

    if not args:
        return result

    for n in args:
        result += n

    return result


def equal(env, *args):
    if not args:
        return True

    first = args[0]
    for i in range(1, len(args)):
        if first != args[i]:
            return False

    return True
