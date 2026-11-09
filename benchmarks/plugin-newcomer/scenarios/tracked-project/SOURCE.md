# Source of this fixture

A trimmed copy of devvm, github.com/modama-rdm/devvm, at commit `2649ab5` (2026-11-09), under its MIT licence (`LICENSE`, kept as it is). Copied: `README.md`, `CLAUDE.md`, `design/requirements.md`, `design/spec.md`, unchanged. Left out: the `devvm` script and everything it runs (`guest/`, `cloud-init/`, `install.sh`, `tests/`): it creates and destroys libvirt VMs, and nothing in a self-test may run it.

`.tracker/` stands for the project's GitHub issue tracker, which the tester cannot reach: `issues.json` and `pulls.json` are `gh issue list` and `gh pr list --state all --json …` as of 2026-11-09, with two changes: the GitHub accounts are replaced by roles, and each author keeps only that role (no name, no id) (`owner` is the maintainer, `second-user` the colleague who tried devvm first), and the body of issue 8 is shortened because it quoted paths of another project.
