---
description: A probe of the eval sandbox, not of a skill. Which python3 runs there and whether it finds its standard library; the skills' start-up line needs it (ledger 290).
max_turns: 6
allowed_tools: [Bash]
---

Run this one Bash command exactly as it stands, then reply with its complete output inside a code block and nothing else:

    echo "PATH=$PATH"; echo "HOME=$HOME"; env | grep -i '^python' || echo 'no PYTHON* variables'; for p in $(which -a python3) /usr/bin/python3; do echo "== $p -> $(readlink -f "$p")"; "$p" -c 'import sys, encodings; print("OK", sys.version.split()[0], sys.prefix)' 2>&1 | tail -2; done; ls -ld /home/*/miniforge3/lib 2>&1 | head -2
