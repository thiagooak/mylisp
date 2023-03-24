import sym
import core as c
import values


def _eval_special_forms(env, v):
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
        return c.loop(env, v[1])

    if v[0] == sym.SymLet:
        local_env = {}
        local_env.update(env)

        for i in range(0, len(v[1]), 2):
            local_env[v[1][i]] = eval_value(local_env, v[1][i+1])

        return c.implicit_do(local_env, v[2:])

    if v[0] == sym.SymIf:
        if (len(v) != 3 and len(v) != 4):
            raise Exception(
                f'Wrong number of args ({len(v)}) passed to: if')
        return c.if_me(env, *v[1:])

    if v[0] == sym.SymCond:
        for i in range(1, len(v), 2):
            result = c.if_me(env, v[i], v[i+1])
            if result:
                return result
        return None

    if v[0] == sym.SymLambda:
        return values.Lambda(env, v[1], v[2])

    return None


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

    if t == values.Vector:
        resolved = list(map(lambda p:  eval_value(env, p), v))
        return values.Vector(resolved)

    if t == list:
        special_form = _eval_special_forms(env, v)
        if special_form:
            return special_form

        resolved = list(map(lambda p:  eval_value(env, p), v))

        function = resolved[0]
        params = resolved[1:]

        return function(env, *params)

    raise Exception(f'Dont know how to evaluate {v}({t})')
