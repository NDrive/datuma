# Datuma

[![PyPI version](https://badge.fury.io/py/datuma.svg)](https://badge.fury.io/py/datuma)

A tool to automate migrations of data between database instances. It allows you
for example, to automate tests based on real production data.

## Database support
At this development stage, the following databases are supported:
- Postgres
- RethinkDB (with python package rethinkdb)
- Redis

## Assumptions
- You can connect by ssh with the servers described in the configuration file
- Sudo is passwordless

# Usage

Create a `datuma.json` to create restores definitions. The following example have
restores with and without containers:

```json
[
  {
    "database": "products",
    "type": "postgres",
    "source": {"server": "db1.company.com", "container": "products_postgres_1", "database": "products"},
    "destination": { "container": "test_products_postgres_1", "database": "products", "drop": true}
  },
  {
    "database": "authentication",
    "type": "rethinkdb",
    "source": {"server": "db2.company.com", "container": "authentication_rethinkdb_1", "database": "auth", "password": "ssd"},
    "destination": { "container": "test_authentication_rethinkdb_1", "database": "auth", "options": "--force"}
  },
  {
    "database": "store",
    "type": "postgres",
    "source": {"server": "db2.company.com", "database": "auth"},
    "destination": { "database": "auth"}
  },
  {
    "database": "cache",
    "type": "redis",
    "source": {"server": "cache1.company.com", "rdb": "/path/to/dump.rdb"},
    "destination": {"address": "localhost", "port": 6379}
  }
]
```

Run all data migrations:

    datuma

Run only data migration of one database:

    datuma products

# Install
Install __Python 3.5__ or later and then:

    pip install datuma

# Development
Use virtualenv with Python 3.5 or later.

## Setup
Working in development mode:

    python setup.py develop

## Publish

    python setup.py register
    python setup.py sdist upload
