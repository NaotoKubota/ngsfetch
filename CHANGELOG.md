# Change log

All notable changes to this ngsfetch project will be documented in this file.

## [v0.1.2] - 2026-08-25

### Changed

- Enhance error handling: remove files on checksum failure.

### Fixed

- Report a non-zero exit code when one or more files fail to download after exhausting retries ([#4](https://github.com/NaotoKubota/ngsfetch/issues/4)).
- Track download results per file instead of counting `*.fastq.gz` files on disk, so a truncated download is no longer reported as `All files downloaded successfully`.
- Remove incomplete `*.fastq.gz` files (and their `.aria2` control files) when a download ultimately fails.

## [v0.1.1] - 2025-03-29

### Added

- Added a Dockefile for building a Docker image.

## [v0.1.0] - 2025-03-29

Initial release of ngsfetch.
