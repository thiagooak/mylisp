import unittest
from symbol import Symbol
from charstream import CharStream, EOF
from reader import read_value
from list import to_lisp_list

class TestReader(unittest.TestCase):

    def test_reader(self):
        cs = CharStream('10 (True False None) a-symbol')
        self.assertEqual(read_value(cs), 10)
        self.assertEqual(read_value(cs), to_lisp_list([True, False, None])) # @BOOK LinkedList.create does not exist
        self.assertEqual(read_value(cs), Symbol('a-symbol')) # @BOOK Symbol.intern does not exist
        self.assertEqual(read_value(cs), EOF)

if __name__ == '__main__':
    unittest.main()
