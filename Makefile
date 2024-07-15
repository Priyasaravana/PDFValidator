install:
		poetry install --no-root

dev:
	  set PYTHONPATH=%cd% && poetry run fastapi dev src/main.py

test:
	  set PYTHONPATH=%cd% && poetry run python src/test_main.py

.PHONY: install dev
