# Patch Notes

## v1.0.0

### Initial Release

This is the first functional release of GH-graph-Automation CLI.

### Added

* Python CLI architecture
* `argparse`
* Configuration validation
* UTF-8 text-file filtering
* Deterministic file-ordering method
* Commit scheduling
* User-defined commits per day
* User-defined commit intervals
* Dry-run mode
* Git staging, committing, and pushing

### Known Issues

* v1.0.0 has a small scope and many issues.
* Source repository and working repository are currently the same directory, meaning the original contents may be modified during execution. This is because I don't get paid enough for this.
* If execution is interrupted, the repository may be left in a partially reconstructed state.
* Many unnecessary comments because the dev was running on coffee and ambition.
* Dry-run mode simulates the execution plan but does not validate every Git operation that would occur during a REAL run.
* Git authentication, remote configuration, and push permissions are assumed to be already configured correctly.
* Files that cannot be decoded as UTF-8 are skipped :)
* The scheduler currently operates using the system's local time and doesn't provide explicit timezone configuration. Shouldn't be a problem if you're Indian. Lol, imagine not being Indian.

### Architecture

This project is divided into focused modules:

* `cli.py`
* `config.py`
* `splitter.py`
* `git.py`
* `scheduler.py`
* `main.py`

 
