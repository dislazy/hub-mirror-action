

class Hub(object):
    def __init__(
        self, src, dst
    ):
        # 切分/前后的 域名 和 用户
        self.src_type, self.src_account = self._split(src, 'src')
        self.dst_type, self.dst_account = self._split(dst, 'dst')
        prefix = 'git@'
        suffix = ':'
        self.src_repo_base = prefix + self.src_type + suffix + self.src_account
        self.dst_repo_base = prefix + self.dst_type + suffix + self.dst_account

    @staticmethod
    def _split(name, field):
        # 必须是 '域名/账号' 两段（如 'github.com/kunpengcompute'），
        # 拼出来的 ssh 地址才是 git@<域名>:<账号>，否则连不上目标端
        parts = str(name).strip().split('/')
        if len(parts) != 2 or not parts[0] or not parts[1]:
            raise ValueError(
                "%s must be in the form of '<hub-domain>/<account>', "
                "e.g. 'github.com/kunpengcompute', got: %r" % (field, name))
        if '.' not in parts[0]:
            # 域名不带点多半是漏写了域名（如 'github/Yikun' 拼出
            # git@github:Yikun，无法解析）。但用户也可能在 ssh config
            # 里配置了主机别名，所以只提示、不报错
            print("WARNING: %s domain '%s' has no dot, you probably want "
                  "something like 'github.com/%s'."
                  % (field, parts[0], parts[1]))
        return parts[0], parts[1]
