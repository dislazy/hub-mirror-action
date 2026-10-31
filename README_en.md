# Hub Mirror Action

English | [简体中文](./README.md)

Action for mirroring repos between Hubs (like Github and Gitee and more)

## Tutorial

```yaml
steps:
- name: Mirror the Github organization repos to Gitee.
  uses: Dislazy/hub-mirror-action@master
  with:
    src: github.com/kunpengcompute
    dst: gitee.com/kunpengcompute
    dst_key: ${{ secrets.GITEE_PRIVATE_KEY }}
    static_list: repo1,repo2,repo3
    cache_path: /github/workspace/hub-mirror-cache
    force_update: true
    debug: true
    timeout: '1h'
    mappings: "yikun.github.com=>blog"
```

Here is a workflow to mirror the kunpengcompute org repos from Github to Gitee, see more complete workflows in [here](https://github.com/Yikun/hub-mirror-action/tree/master/.github/workflows).

## Usage

#### Required
- `src` source account, such as `github.com/kunpengcompute`, is the Github kunpengcompute account.
- `dst` Destination account, such as `gitee.com/kunpengcompute`, is the Gitee kunpengcompute account.
- `dst_key` the private key to push code in destination account (default in ~/.ssh/id_rsa), you can see [generating SSH keys](https://docs.github.com/articles/generating-an-ssh-key/) to generate the pri/pub key, and make sure the pub key has been added in destination. You can set Github ssh key in [here](https://github.com/settings/keys)，set the Gitee ssh key in [here](https://gitee.com/profile/sshkeys).
- `static_list` Only mirror repos in the static list, like 'repo1,repo2,repo3'. **Required and must not be empty**: an empty list fails the action instead of silently doing nothing.
- `src`/`dst` must be two segments '<hub-domain>/<account>' (e.g. `github.com/kunpengcompute`). A wrong format fails with a clear error; a domain without a dot (e.g. `github/Yikun`) only logs a warning.

#### Optional
- `cache_path` (optional) let code clone in specific path, can be used with actions/cache to speed up mirror.
- `force_update` (optional) Force to update the destination repo, use '-f' flag do 'git push'
- `timeout` (optional) Default is '30m', set the timeout for every git command, like '600'=>600s, '30m'=>30 mins, '1h'=>1 hours. Invalid values (e.g. `30M`) fall back to `30m` with a log hint; explicit `0` still means no timeout.
- `mappings` (optional) Default is empty, the source repos mappings, such as 'A=>B, C=>CC', source repo name would be mapped follow the rule: A to B, C to CC. Mapping is not transitive.

## Environment

- The base image is pinned to `ubuntu:24.04` instead of the floating `ubuntu` tag (that tag jumping from 20.04 to 24.04 changed OpenSSH and pip defaults and broke the action).
- Python dependencies are pinned in [`hub-mirror/requirements.txt`](./hub-mirror/requirements.txt) and installed **at image build time**, so runs no longer hit PyPI.
- `StrictHostKeyChecking no` is kept, and `ssh-rsa` is re-enabled to stay compatible with the old OpenSSH 8.2 defaults and legacy hubs. Remove the two lines in `Dockerfile` if you want a stricter policy.
- `git safe.directory` is set in the image, so a cache dir restored by `actions/cache` does not fail with `dubious ownership`.
- [`.github/dependabot.yml`](./.github/dependabot.yml) tracks actions / pip / docker versions weekly.

## FAQ
- How to use `secrets` to add key?

  You can use below steps to add secrets, you can also see more in [Secrets](https://help.github.com/en/actions/configuring-and-managing-workflows/creating-and-storing-encrypted-secrets).

  1. **Add Secrets**，add settings-secrets in repo，like `GITEE_PRIVATE_KEY`、`GITEE_TOKEN`
  2. **Add workflow**，add the workflow file into .github/workflows.

## Reference
- [Hub mirror template](https://github.com/yi-Xu-0100/hub-mirror): A template repo to show how to use this action. from @yi-Xu-0100
- [Auto-Sync GitHub Repositories to Gitee](https://github.com/ShixiangWang/sync2gitee): An introduction about how to use this action. from @ShixiangWang
- [Use Github Action to sync reois to Gitee](http://yikun.github.io/2020/01/17/%E5%B7%A7%E7%94%A8Github-Action%E5%90%8C%E6%AD%A5%E4%BB%A3%E7%A0%81%E5%88%B0Gitee/): The blog for this action.
- [Hub Mirror Action](https://github.com/Yikun/hub-mirror-action): This before repo,greate
