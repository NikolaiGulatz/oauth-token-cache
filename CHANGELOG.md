# Changelog

All notable changes to this project will be documented in this file.


The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 0.3.0 - 2021-05-11

### Changed

- Updated [redis-py](https://github.com/andymccurdy/redis-py) from `3.3.11` to `3.5.3`
- Switched from `hmset` to `hset` since `hmset` has been deprecated in [redis-py:3.5.0](https://github.com/andymccurdy/redis-py/blob/master/CHANGES#L28)

## 0.2.0 - 2020-02-20

### Added

- Added ability to overwrite returned access tokens via `OAUTH_TOKEN` environment variable

### Fixed

- Fixed a bug where when passing a custom redis client, the connection was still tested using the default client, fixed by [@janjagusch](https://github.com/janjagusch)

## 0.1.0 - 2019-10-29

### Added

- Added initial functionality
