import unittest
from list import List, to_lisp_list

class TestList(unittest.TestCase):

    def test_list(self):
        numbers_1 = List(3, None)
        numbers_2 = List(2, numbers_1)
        numbers = List(1, numbers_2)

        self.assertEqual(numbers.first(), 1)
        self.assertEqual(numbers.rest().first(), 2)
        self.assertEqual(numbers.rest().rest().first(), 3)

    def test_to_lisp_list(self):
        numbers = to_lisp_list([1, 2, 3])
        self.assertEqual(str(numbers), '(1 2 3)')
        self.assertEqual(numbers.first(), 1)
        self.assertEqual(numbers.rest().first(), 2)
        self.assertEqual(numbers.rest().rest().first(), 3)

if __name__ == '__main__':
    unittest.main()
