import unittest

from hub import Hub
from mirror import Mirror


class TestMirror(unittest.TestCase):

    def _hub(self):
        return Hub('github.com/a', 'gitee.com/b')

    def test_urls(self):
        m = Mirror(self._hub(), 'r1', 'r2', cache='/tmp/cache')
        self.assertEqual(m.src_url, 'git@github.com:a/r1.git')
        self.assertEqual(m.dst_url, 'git@gitee.com:b/r2.git')
        self.assertEqual(m.repo_path, '/tmp/cache/r1')

    def test_timeout_valid(self):
        self.assertEqual(Mirror(self._hub(), 'r', 'r', timeout='600').timeout,
                         600)
        self.assertEqual(Mirror(self._hub(), 'r', 'r', timeout='30m').timeout,
                         1800)
        self.assertEqual(Mirror(self._hub(), 'r', 'r', timeout='1h').timeout,
                         3600)
        # 显式传 0 仍然表示不限时
        self.assertEqual(Mirror(self._hub(), 'r', 'r', timeout='0').timeout, 0)

    def test_timeout_invalid_falls_back_to_30m(self):
        # 非法值不能静默变成 0（不限时），必须回退到默认 30m
        for bad in ['30M', '1H', 'm30', 'abc', '']:
            m = Mirror(self._hub(), 'r', 'r', timeout=bad)
            self.assertEqual(m.timeout, 1800, msg=bad)


if __name__ == '__main__':
    unittest.main()
