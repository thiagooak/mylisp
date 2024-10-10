from symbol import Symbol
from streams import ConsoleCharStream
from reader import read_value, EOF
from list import List, to_lisp_list

def ml_print(_environment, args):
    while args:
        if args.rest():
            print(args.first(), end=' ')
        else:
            print(args.first())
        args = args.rest()

def eval_items(environment, lst):
    """Evaluate each item in a list, return a list of the results."""
    evaled = []
    while lst:
        evaled.append(eval_value(environment, lst.first()))
        lst = lst.rest()
    return to_lisp_list(evaled)

# # Our first cut at eval_function_call, which is not quite right.
# # Can you see the problem?
# def eval_function_call(environment, lst):
#     # The missing bit: First evaluate all of the items in the list.
#     evaled_list = eval_items(environment, lst)
#
#     # Get the first item on the list which will be the function.
#     f = evaled_list.first()
#
#     # And the rest of the items are the arguments.
#     args = evaled_list.rest()
#     # ...and call the function, returning the result.
#     return f(environment, args)

# A handy constant.
SYM_DEF = Symbol('def')
SYM_QUOTE = Symbol('quote')
SYM_IF = Symbol('if')
SYM_WHILE = Symbol('while')
SYM_LET = Symbol('let')
SYM_FOR = Symbol('for')
SYM_DEFN = Symbol('defn')
SYM_LAMBDA = Symbol('lambda')

class Lambda:
    def __init__(self, env, params, body):
        self.env = env
        self.params = params
        self.body = body

    def __call__(self, _env, args):
        local_env = make_env(self.env)
        params = self.params
        while args:
            local_env[params.first()] = args.first()
            params = params.rest()
            args = args.rest()
        return eval_value(local_env, self.body)

def eval_list(env, lst):
    verb = lst.first()
    if verb == SYM_DEF:
        name = lst.second()
        value = lst.third()
        evaled_value = eval_value(env, value)
        env[name] = evaled_value
        result = name
    elif verb == SYM_QUOTE:
        result = lst.second()
    elif verb == SYM_IF:
        condition = lst.second()
        true_expr = lst.third()
        if lst.rest().rest().rest():
            false_expr = lst.fourth()
        else:
            false_expr = None
        if eval_value(env, condition):
            result = eval_value(env, true_expr)
        else:
            result = eval_value(env, false_expr)
    elif verb == SYM_WHILE:
        condition = lst.second()
        body = lst.third()
        result = None
        while eval_value(env, condition):
            result = eval_value(env, body)
    elif verb == SYM_LET:
        bindings = lst.second()
        body = lst.third()
        local_env = make_env(env)
        while bindings:
            name = bindings.first()
            value = bindings.second()
            local_env[name] = eval_value(local_env, value)
            bindings = bindings.rest().rest()
        result = eval_value(local_env, body)
    elif verb == SYM_FOR:
        raise Exception("Not implemented")
    elif verb == SYM_LAMBDA:
        params = lst.second()
        body = lst.third()
        result = Lambda(env, params, body)
    elif verb == SYM_DEFN:
        name = lst.second()
        params = lst.third()
        body = lst.fourth()
        f = Lambda(env, params, body)
        env[name] = f
        result = name
    else:
        evaled_lst = eval_items(env, lst)
        f = evaled_lst.first()
        args = evaled_lst.rest()
        result = f(env, args)
    return result


def eval_value(env, value):
    if isinstance(value, Symbol):
        return lookup(env, value)
    elif isinstance(value, List):
        return eval_list(env, value)
    return value

def repl(env, stream):
    value = read_value(stream)
    while value != EOF:
        result = eval_value(env, value)
        print(result)
        value = read_value(stream)

# MyLisp addition.
# How would you implement the subtract, multiply and divide functions?
def ml_add(environment, args):
    return args.first() + args.second()

# MyLisp equality.
# How would you implement the less than, less than or equal, etc?
def ml_equals(environment, args):
    return args.first() == args.second()

# MyLisp logical AND function.
# How would you implement or, xor and not?
def ml_and(environment, args):
    return args.first() == args.second()

def ml_first(environment, args):
    lst = args.first()
    return lst.first()

def ml_rest(environment, args):
    lst = args.first()
    return lst.rest()

def ml_cons(environment, args):
    item = args.first()
    lst = args.second()
    return List(item, lst)

def ml_dir(environment, args):
    return to_lisp_list(environment.keys())

SYM_PARENT = Symbol('*parent*')

def make_env(parent=None):
    return {SYM_PARENT: parent}

def lookup(env, s):
    if s in env:
        return env[s]

    parent = env[SYM_PARENT]
    if parent:
        return lookup(parent, s)

    raise Exception(f'Symbol not found in environment: {s}')

def root_env():
    env = make_env()
    env[Symbol('language')] = 'MyLisp'
    env[Symbol('version')] = 1
    env[Symbol('print')] = ml_print
    env[Symbol('+')] = ml_add
    env[Symbol('==')] = ml_equals
    env[Symbol('and')] = ml_and
    env[Symbol('first')] = ml_first
    env[Symbol('rest')] = ml_rest
    env[Symbol('cons')] = ml_cons
    env[Symbol('dir')] = ml_dir
    # What would you do here for -, *, /, <, <=, >, >=, or, xor and not?
    return env

# Set up the environment dictionary and pass it to repl.
# Add a couple of predefined bindings while we are at it.
if __name__ == '__main__':
    environment = root_env()
    stream = ConsoleCharStream()
    repl(environment, stream)


