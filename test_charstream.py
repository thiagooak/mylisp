import unittest
from charstream import CharStream, EOF

class TestCharStream(unittest.TestCase):

    def test_methods(self):
        cs = CharStream('123')
        self.assertEqual(cs.read(), '1')
        self.assertEqual(cs.peek(), '2')
        self.assertEqual(cs.peek(), '2')
        self.assertEqual(cs.read(), '2')
        self.assertEqual(cs.read(), '3')
        self.assertEqual(cs.read(), EOF)

if __name__ == '__main__':
    unittest.main()