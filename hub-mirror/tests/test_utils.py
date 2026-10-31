import unittest
from utils import str2map, str2list, cov2sec


class TestUtils(unittest.TestCase):

    def test_str2map(self):
        self.assertEqual(str2map("a=>b, c=>d"), {'a': 'b', 'c': 'd'})
        self.assertEqual(str2map("a=>b,c=>d"), {'a': 'b', 'c': 'd'})
        # No transitivity
        self.assertEqual(str2map("cc=>c,c=>d"), {'cc': 'c', 'c': 'd'})

    def test_str2map_empty(self):
        self.assertEqual(str2map(''), {})
        self.assertEqual(str2map(None), {})

    def test_str2list(self):
        self.assertEqual(str2list("a, b"), ['a', 'b'])
        self.assertEqual(str2list("a,b"), ['a', 'b'])
        self.assertEqual(str2list('a ,b '), ['a', 'b'])

    def test_str2list_empty(self):
        self.assertEqual(str2list(''), [])
        self.assertEqual(str2list(None), [])

    def test_cov2sec(self):
        self.assertEqual(cov2sec('600'), 600)
        self.assertEqual(cov2sec('30m'), 1800)
        self.assertEqual(cov2sec('1h'), 3600)
        self.assertEqual(cov2sec('1d'), 86400)


if __name__ == '__main__':
    unittest.main()
