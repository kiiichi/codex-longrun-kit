.PHONY: test smoke detect

test:
	python -m pytest

detect:
	python .agents/skills/codex-longrun-init/scripts/detect_stack.py --repo-root . --format markdown

smoke:
	rm -rf /tmp/codex-longrun-smoke
	python .agents/skills/codex-longrun-init/scripts/init_longrun.py --repo-root /tmp/codex-longrun-smoke --task-brief "Smoke test" --force
	find /tmp/codex-longrun-smoke/docs -maxdepth 3 -type f | sort
