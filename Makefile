PY ?= python3
export PYTHONPATH := src:.

.PHONY: install test cli serve lint clean

install:
	$(PY) -m pip install -r requirements.txt
	$(PY) -m pip install -e .

test:
	$(PY) -m pytest tests -q

cli:
	$(PY) -m jyotish.cli --date 1990-04-14 --time 08:15 \
		--lat 13.0827 --lon 80.2707 --tz 5.5 --place Chennai

serve:
	$(PY) -m uvicorn app.main:app --reload --port 8000

clean:
	find . -name __pycache__ -type d -exec rm -rf {} +
	rm -rf .pytest_cache build dist *.egg-info
