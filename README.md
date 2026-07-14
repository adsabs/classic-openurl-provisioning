# OpenURL Provisioning Utility

A command-line utility for maintaining the `library` table in the
institute PostgreSQL database (hosted on AWS), which holds OpenURL
server information used to resolve links to institutional libraries.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt        # runtime dependencies
pip install -r dev-requirements.txt    # pytest, for running the test suite
```

## Configuration

Configuration values live in `config.py`. A `local_config.py` file, if
present, overrides values from `config.py` and is where
environment/deployment-specific settings (database credentials, the
real path to the OpenURL data file, etc.) belong.

Key settings:

| Setting | Purpose |
|---|---|
| `SQLALCHEMY_DATABASE_URI` | Connection string for the institute database |
| `INSTITUTE_OPENURL_DATA` | Path to the two-column (name, server URL) OpenURL data file |
| `INSTITUTE_LOGGING` | Standard `logging.config.dictConfig` dictionary |

## Usage

```bash
python run.py updatedb   # sync the library table from the OpenURL data file
python run.py exportdb   # print the current contents of the library table
```

`updatedb` reads `INSTITUTE_OPENURL_DATA` (tab-separated: organization
name, OpenURL server URL) and adds, updates, or removes rows in the
`library` table so it matches the file. Malformed or empty lines are
skipped and reported on stderr rather than aborting the run.

`exportdb` prints every `library` row as `name\tserver`.

## Tests

```bash
pytest tests/
```

Tests run against a temporary SQLite database and do not touch the
production database.
