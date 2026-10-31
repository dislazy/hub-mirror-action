#!/bin/bash
#
# Parameter hand-off only: git, ssh and the pinned python venv already live in
# the image (see Dockerfile), so nothing is installed at run time any more.
# Every input arrives as INPUT_* from action.yml.

DEBUG="${INPUT_DEBUG}"

if [[ "$DEBUG" == "true" ]]; then
  set -x
fi

mkdir -p /root/.ssh
printf '%s\n' "${INPUT_DST_KEY}" > /root/.ssh/id_rsa
chmod 600 /root/.ssh/id_rsa

# exec keeps the exit code of the mirror run, same as the old `exit $?`.
exec python3 /hub-mirror/hubmirror.py --src "${INPUT_SRC}" --dst "${INPUT_DST}" \
  --cache-path "${INPUT_CACHE_PATH}" \
  --static-list "${INPUT_STATIC_LIST}" \
  --force-update "${INPUT_FORCE_UPDATE}" \
  --debug "${INPUT_DEBUG}" \
  --timeout "${INPUT_TIMEOUT}" \
  --mappings "${INPUT_MAPPINGS}"
