python-virtualenv: .python-version

.python-version:
	@if ! pyenv versions --bare | grep -qx "3.10.16"; then \
		pyenv install 3.10.16; \
	fi
	@if ! pyenv virtualenvs --bare | grep -qx "nyt-3.10.16"; then \
		pyenv virtualenv 3.10.16 nyt-3.10.16; \
	fi
	pyenv local nyt-3.10.16
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

run:
	./nyt-fun-ruin.py

check:
	ruff check

fix:
	ruff check --fix

.PHONY: python-virtualenv run check fix