import unittest

from hub import Hub


class TestHub(unittest.TestCase):

    def test_split(self):
        hub = Hub('github.com/kunpengcompute', 'gitee.com/kunpengcompute')
        self.assertEqual(hub.src_type, 'github.com')
        self.assertEqual(hub.src_account, 'kunpengcompute')
        self.assertEqual(hub.src_repo_base, 'git@github.com:kunpengcompute')
        self.assertEqual(hub.dst_repo_base, 'git@gitee.com:kunpengcompute')

    def test_strip_whitespace(self):
        hub = Hub(' github.com/a ', 'gitee.com/b')
        self.assertEqual(hub.src_repo_base, 'git@github.com:a')

    def test_invalid_format(self):
        bad_values = [
            '',                      # empty
            'github',                # no account
            'github.com/a/b',        # too many segments
            'https://github.com/a',  # url style, not 'domain/account'
            'github.com/',           # empty account
        ]
        for bad in bad_values:
            with self.assertRaises(ValueError, msg=bad):
                Hub(bad, 'gitee.com/kunpengcompute')
            with self.assertRaises(ValueError, msg=bad):
                Hub('github.com/kunpengcompute', bad)


if __name__ == '__main__':
    unittest.main()
