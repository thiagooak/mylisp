class List:
    """A traditional Lispy linked list. """
    def __init__(self, first, rest):
      self._first = first
      self._rest = rest

    def first(self):
        return self._first

    def rest(self):
        return self._rest

    def second(self):
        return self.rest().first()

    def third(self):
        return self.rest().rest().first()

    def fourth(self):
        return self.rest().rest().rest().first()

    def __repr__(self):
        result = '('
        l = self
        while l:
            result += str(l._first)
            if l._rest:
                result += ' '
            l = l._rest
        result += ')'
        return result

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, List):
            return False

        l1 = self
        l2 = other
        while l1 and l2:
            if l1.first() != l2.first():
                return False
            l1 = l1.rest()
            l2 = l2.rest()
        return (l1 is None) and (l2 is None)

def to_lisp_list(py_list):
    result = None
    for v in reversed(py_list):
        result = List(v, result)
    return result

def to_python_list(lisp_list):
    result = []
    while lisp_list:
        result.append(l_list.first())
    l_list = l_list.rest()
    return result