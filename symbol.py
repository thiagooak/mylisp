class Symbol:
    def __init__(self, name):
      self._name = name

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, Symbol): # @BOOK inverted params
            return False
        return self._name == other._name

    def __repr__(self):
        return self._name

    def __hash__(self):
        return hash(self._name)