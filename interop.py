import importlib as il
import sym

def do_import(env, mod_name):
    """Import a Python module full of native functions
       into the given env. Each native function is
       bound to mod-name/f-name."""
    result = {}
    m = il.import_module(mod_name, sym)
    names = dir(m)
    for n in names:
        name = sym.Symbol.intern(f'{mod_name}/{n}')
        result[name] = getattr(m, n)

    env.update(result)
    return mod_name


def bang(env, f, *args):
    """Given a form that looks like (! native-f arg1 arg2...)
    execute the native function and return the result."""
    return f(*args)


def dot(env, obj, *names):
    """Given a form that looks like (. py-object field1 field2...)
    drill down into the object attributes and return the value."""
    for n in names:
        obj = getattr(obj, str(n))
    return obj

def dot_bang(env, obj, names, *args):
    """Given a form that looks like (. py-object [field1 field2 ...] arg1 arg2 ..)
    drill down into the object attributes then call the resulting method with
    the arguments given."""
    method = None
    for n in names:
        method = getattr(obj, str(n))
    return method(*args)
