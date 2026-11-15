#!/usr/bin/env python3
"""Run one problem in its own directory and its own git repository.

    python3 run_autoresearch.py P-3

The process detaches and returns at once. A second call on a problem that
already has a run directory resumes it. Each problem's directory contains its
own .git, so two problems running at the same time never touch the same index,
HEAD, or lock. The only thing they share is the read-only virtualenv symlink.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GROK = os.environ.get("GROK_BIN", "grok")
REMOTE = "git@git.29tech.cn:qshsit/physics-intern-parallel.git"


def git(run: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(run), *args], check=True,
                   capture_output=True, text=True)


def main() -> int:
    if len(sys.argv) != 2 or not sys.argv[1].startswith("P-"):
        print("usage: run_autoresearch.py P-<n>", file=sys.stderr)
        return 2
    pass_id = sys.argv[1]

    src = ROOT / "problems" / f"{pass_id}.md"
    if not src.is_file():
        print(f"no statement at {src}", file=sys.stderr)
        return 1

    run = ROOT / "runs" / pass_id
    for sub in ("computations/.briefs", "derivations/.briefs",
                "critiques", "notes", "references", "data"):
        (run / sub).mkdir(parents=True, exist_ok=True)
    for name in ("prompts", "skills", ".grok"):
        dest = run / name
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(ROOT / name, dest)
    for name in ("AGENTS.md", "package.json"):
        shutil.copy(ROOT / name, run / name)
    (run / ".venv").unlink(missing_ok=True)
    (run / ".venv").symlink_to(ROOT / ".venv")
    shutil.copy(src, run / "problem.md")

    template = (ROOT / "prompts" / "run-template.md").read_text()
    (run / "notes" / "autoresearch-prompt.md").write_text(
        template.replace("__PASS__", pass_id))

    # A pass commits after every step. Its commits go to refs/heads/<pass id>
    # on the shared remote, and its index lives inside its own .git, so two
    # passes never take the same lock.
    if not (run / ".git").exists():
        git(run, "init", "-q", "-b", pass_id)
        git(run, "remote", "add", "origin", REMOTE)
        (run / ".gitignore").write_text(".venv\n")
        git(run, "add", "-A")
        git(run, "-c", "commit.gpgsign=false", "commit", "-q",
            "-m", f"{pass_id}: workspace initialised")

    if os.fork():
        return 0
    os.setsid()
    os.chdir(run)
    log = open(run / "autoresearch.log", "a")
    os.dup2(log.fileno(), 1)
    os.dup2(log.fileno(), 2)
    os.execvp(GROK, [
        GROK, "--trust", "--always-approve", "--max-turns", "150",
        "--cwd", str(run),
        "--single", (run / "notes" / "autoresearch-prompt.md").read_text(),
    ])


if __name__ == "__main__":
    sys.exit(main())
