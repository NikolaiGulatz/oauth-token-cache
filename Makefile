.PHONY: test

test:
	@poetry run tox

black:
	@poetry run black --check .

pylint:
	@poetry run pylint oauth_token_cache
