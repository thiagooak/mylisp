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


class SymbolNotFoundError(Exception):
    def __init__(self, symbol, message=None):
        if message:
            self.message = message
        else:
            self.message = f'Symbol not found {symbol}'

        self.symbol = symbol
        super().__init__(self.message)


SymFn = Symbol.intern('fn')
SymDef = Symbol.intern('def')
SymLoop = Symbol.intern('loop')
SymLet = Symbol.intern('let')
SymQuote = Symbol.intern('quote')


