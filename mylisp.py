#!python3

import sys
import re
import readline
from sym import Symbol, SymbolNotFoundError
from reader import ConsoleReader, FileReader, read_value, SymQuote

SymFn = Symbol.intern('fn')
SymDef = Symbol.intern('def')
SymLoop = Symbol.intern('loop')
SymLet = Symbol.intern('let')


def to_string(v):
    t = type(v)

    if t == int:
        return str(v)

    if t == str:
        return '"' + v + '"'

    if t == Symbol:
        return v.name

    if t == list:
        result = []
        for i in v:
            result.append(to_string(i))
        return '(' + ' '.join(result) + ')'


def source(env, path):
    reader = FileReader(path)
    repl(env, reader)


def read(env):
    reader = ConsoleReader(prompt='> ')
    while True:
        x = read_value(reader.getc)
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
        x = read_value(reader.getc)
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


def eval_value(env, v):
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
                raise Exception(
                    f'Wrong number of args ({len(v)}) passed to: def')
            name = v[1]
            value = v[2]
            env[name] = eval_value(env, value)
            return value

        if v[0] == SymQuote:
            return v[1]

        if v[0] == SymLoop:
            return loop(env, v[1])

        if v[0] == SymLet:
            local_env = {}
            local_env.update(env)

            for i in range(0, len(v[1]), 2):
                local_env[v[1][i]] = eval_value(local_env, v[1][i+1])

            return implicit_do(local_env, v[2:])

        resolved = list(map(lambda p:  eval_value(env, p), v))

        function = resolved[0]
        params = resolved[1:]

        return function(env, *params)

    raise Exception(f'Dont know how to evaluate {v}({t})')


Env = {Symbol.intern('version'): 100, Symbol.intern(
    'add'): add, Symbol.intern('read'): read, Symbol.intern('eval'): eval_value, Symbol.intern('print'): print_me}


def main() -> int:
    if (len(sys.argv) == 2):
        source(Env, sys.argv[1])
        return 0

    source(Env, "./startup.mylisp")

    return 0


if __name__ == '__main__':
    sys.exit(main())
