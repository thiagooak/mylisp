#!python3

import sys
import re
import readline
from sym import Symbol, SymbolNotFoundError
from reader import ConsoleReader, read_value, SymQuote

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


def read(env):
    reader = ConsoleReader()
    while True:
        x = read_value(reader.getc)
        if x == None:
            break
        return x


def eval(env, v):
    return eval_value(v, env)


def print_me(env, v):
    print(to_string(v))


def loop(env, v):
    while True:
        (eval_value(v, env))


def repl(env, reader):
    while True:
        x = read_value(reader.getc)
        if x == None:
            break
        print(to_string(eval_value(x, env)))


def add(env, *args):
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
                raise Exception(
                    f'Wrong number of args ({len(v)}) passed to: def')
            name = v[1]
            value = v[2]
            env[name] = eval_value(value, env)
            return value

        if v[0] == SymQuote:
            return v[1]

        if v[0] == SymLoop:
            return loop(env, v[1])

        if v[0] == SymLet:
            # implement reader for vectors
            # add v[1] to a copy of env
            # call v[2] with the new env
            # should this be a loop on v[2:]?
            print("v", v)
            print("1", v[1])
            print("2", v[2])
            return eval_value(v[2], env)

        resolved = list(map(lambda p:  eval_value(p, env), v))

        function = resolved[0]
        params = resolved[1:]

        return function(env, *params)

    # @TODO
    # read — reads a lisp expression from the terminal
    # eval — we already talked about this
    # print — prints a lisp expression to the terminal
    # loop — takes an expression and evaluates it over and over, endlessly.
    #
    # we are trying to get to the point where we can write something like this:
    # (loop (print(eval(read))))
    #
    # @TODO let

    raise Exception(f'Dont know how to evaluate {v}({t})')


Env = {Symbol.intern('version'): 100, Symbol.intern(
    'add'): add, Symbol.intern('read'): read, Symbol.intern('eval'): eval, Symbol.intern('print'): print_me}


def main() -> int:
    cr = ConsoleReader()

    print(f'MyLISP: I know how to evaluate a few things.')
    print(f'MyLISP: Make me smarter!')
    repl(Env, cr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
