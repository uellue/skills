#!/bin/bash
# Start the next field-test recording (runbook: design/field-tests/devvm-runbook.md, "Recording, always first").
#
#   record.sh            records into the next free run-<n> under ~/field-test (run-0 the first time), until `exit`
#   record.sh --next     only prints the folder the next recording would use
#
# FIELD_TEST_DIR overrides ~/field-test. Output and timing only: never --log-in, which would record every key,
# passwords included. An existing run folder is never reused or touched; nothing is deleted.
set -euo pipefail

base="${FIELD_TEST_DIR:-$HOME/field-test}"
n=0
for d in "$base"/run-*; do
    [ -d "$d" ] || continue
    k="${d##*/run-}"
    case "$k" in '' | *[!0-9]*) continue ;; esac
    k=$((10#$k))
    [ "$k" -ge "$n" ] && n=$((k + 1))
done
run="$base/run-$n"

if [ "${1:-}" = "--next" ]; then
    echo "$run"
    exit 0
fi
[ $# -eq 0 ] || { echo "usage: record.sh [--next]" >&2; exit 2; }

mkdir -p "$base"
mkdir "$run"  # fails rather than reuse a folder another terminal just took
echo "Recording into $run until you type exit. Output and timing only; look through session.log before sharing it."
exec script -q -T "$run/timing.log" -O "$run/session.log"
