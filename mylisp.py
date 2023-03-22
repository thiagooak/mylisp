#!python3

import sys
import sym
import core as c
import eval as e
import reader as r
import interop


def setenv(env, name, value):
    if isinstance(name, str):
        name = sym.Symbol.intern(name)
    env[name] = value


Env = {}
setenv(Env, '+', c.add)
setenv(Env, '=', c.equal)
setenv(Env, 'read', c.read)
setenv(Env, 'eval', e.eval_value)
setenv(Env, 'print', c.print_me)
setenv(Env, 'import', interop.do_import)
setenv(Env, '!', interop.bang)
setenv(Env, '.', interop.dot)


def main() -> int:
    if (len(sys.argv) == 2):
        c.source(Env, sys.argv[1])
        return 0

    c.source(Env, "./startup.mylisp")
    return 0


if __name__ == '__main__':
    sys.exit(main())
