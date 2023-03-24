import sym
import eval as e

class Vector(list):
    pass

class Lambda():
    def __init__(self, env, params, body):
        self.env = env
        self.params = params
        self.body = body

    def __call__(self, env, *args):
        let_params = []
        for i in range(len(args)):
            let_params.append(self.params[i])
            let_params.append(args[i])
        return e.eval_value(self.env, [sym.SymLet, let_params, self.body])
