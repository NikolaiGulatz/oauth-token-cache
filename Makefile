.PHONY: test

tox:
	@poetry run tox

black:
	@poetry run black --check .

pylint:
	@poetry run pylint oauth_token_cache

pytest:
	@poetry run pytest --cov=oauth_token_cache --cov-report term-missing test/
