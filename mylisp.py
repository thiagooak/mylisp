#!python3

import sys
import re
import readline
import sym
import reader as r
import interop


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
    repl(env, reader)


def read(env):
    reader = r.ConsoleReader(prompt='> ')
    while True:
        x = reader.read_value()
        if x == None:
            break
        return x


def print_me(env, v):
    print(to_string(v))


def loop(env, v):
    while True:
        (eval_value(env, v))


def repl(env, reader):
    while True:
        x = reader.read_value()
        if x == None:
            break
        print(to_string(eval_value(env, x)))


def implicit_do(env, exprs):
    result = None
    for i in range(len(exprs)):
        result = eval_value(env, exprs[i])
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


def eval_value(env, v):
    t = type(v)

    if t == int:
        return v

    if t == str:
        return v

    if t == sym.Symbol:
        if v in env:
            return env[v]
        return sym.SymbolNotFoundError(v)

    if t == list:
        if v[0] == sym.SymDef:
            if len(v) != 3:
                raise Exception(
                    f'Wrong number of args ({len(v)}) passed to: def')
            name = v[1]
            value = v[2]
            env[name] = eval_value(env, value)
            return value

        if v[0] == sym.SymQuote:
            return v[1]

        if v[0] == sym.SymLoop:
            return loop(env, v[1])

        if v[0] == sym.SymLet:
            local_env = {}
            local_env.update(env)

            for i in range(0, len(v[1]), 2):
                local_env[v[1][i]] = eval_value(local_env, v[1][i+1])

            return implicit_do(local_env, v[2:])

        if v[0] == sym.SymIf:
            if (len(v) != 4):
                raise Exception(
                    f'Wrong number of args ({len(v)}) passed to: if')

            if eval_value(env, v[1]):
                return eval_value(env, v[2])

            return eval_value(env, v[3])

        if v[0] == sym.SymCond:
            for i in range(1, len(v), 2):
                if (eval_value(env, v[i])):
                    return eval_value(env, v[i+1])
            return None

        resolved = list(map(lambda p:  eval_value(env, p), v))

        function = resolved[0]
        params = resolved[1:]

        return function(env, *params)

    raise Exception(f'Dont know how to evaluate {v}({t})')


def setenv(env, name, value):
    if isinstance(name, str):
        name = sym.Symbol.intern(name)
    env[name] = value


Env = {}
setenv(Env, '+', add)
setenv(Env, '=', equal)
setenv(Env, 'read', read)
setenv(Env, 'eval', eval_value)
setenv(Env, 'print', print_me)
setenv(Env, 'import', interop.do_import)
setenv(Env, '!', interop.bang)
setenv(Env, '.', interop.dot)


def main() -> int:
    if (len(sys.argv) == 2):
        source(Env, sys.argv[1])
        return 0

    source(Env, "./startup.mylisp")

    return 0


if __name__ == '__main__':
    sys.exit(main())
