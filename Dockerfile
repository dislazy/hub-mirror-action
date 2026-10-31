# Base image is pinned on purpose: the floating `ubuntu` tag jumped from 20.04
# to 24.04 and silently changed the OpenSSH and pip defaults, which is what broke
# this action.
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    GIT_TERMINAL_PROMPT=0 \
    PATH=/opt/venv/bin:$PATH

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        git \
        openssh-client \
        python3 \
        python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Keep the "never check host keys" behaviour of this action, and keep accepting
# legacy ssh-rsa keys/servers: the previous Ubuntu 20.04 base shipped OpenSSH 8.2
# where ssh-rsa was still enabled by default (>= 8.8 disables it, so an existing
# RSA key pointed at an old hub would suddenly stop working).
RUN printf '%s\n' \
        'Host *' \
        '    StrictHostKeyChecking no' \
        '    PubkeyAcceptedAlgorithms +ssh-rsa' \
        '    HostKeyAlgorithms +ssh-rsa' \
        >> /etc/ssh/ssh_config

# git >= 2.35 refuses to touch a repository owned by another uid, which happens
# when actions/cache restores the cache dir under a different owner.
RUN git config --system --add safe.directory '*'

COPY hub-mirror /hub-mirror
COPY action.yml /
COPY entrypoint.sh /

# Install the pinned dependencies once at build time. The previous entrypoint
# created a venv and hit PyPI on every single run, which made the action slow
# and fail whenever PyPI was unreachable.
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir -r /hub-mirror/requirements.txt \
    && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
