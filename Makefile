.PHONY: requirements
requirements:
	pip install -r requirements.txt

.PHONY: lint
lint:
	flake8
	mypy src
	black --check .
	isort --check .

.PHONY: fix_lint
fix_lint:
	black .
	isort .