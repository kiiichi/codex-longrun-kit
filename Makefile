.PHONY: test smoke package

test:
	python -m unittest discover -s tests

smoke:
	rm -rf /tmp/codex-longrun-kit-smoke
	python scripts/init_longrun.py --target /tmp/codex-longrun-kit-smoke --profile standard --task-brief "Smoke task"
	python scripts/freeze_review.py --target /tmp/codex-longrun-kit-smoke --base HEAD
	python scripts/normalize_reviews.py --target /tmp/codex-longrun-kit-smoke

package:
	cd .. && python -m zipfile -c codex-longrun-kit.zip codex-longrun-kit
