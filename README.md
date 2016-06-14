# Datuma

A tool to automate migrations of data between database instances. It allows you
for example, to automate tests based on real production data.

## Database support
At this development stage, only __Docker containers are supported__ with the following databases:
- Postgres
- RethinkDB (with python package rethinkdb)

## Assumptions
- You can connect by ssh with the servers described in the configuration file
- Sudo is passwordless (to run Docker commands)

# Usage

Create a `datuma.json` to create restores definitions:

```json
[
  {
    "database": "products",
    "type": "postgres",
    "source": {"server": "db1.company.com", "container": "products_postgres_1", "database": "products"},
    "destination": { "container": "test_products_postgres_1", "database": "products"}
  },
  {
    "database": "authentication",
    "type": "rethinkdb",
    "source": {"server": "db2.company.com", "container": "authentication_rethinkdb_1", "database": "auth"},
    "destination": { "container": "test_authentication_rethinkdb_1", "database": "auth"}
  }
]
```

Run all data migrations:

    datuma

Run only data migration of one database:

    datuma products

# Install
Install __Python 3.5__ or later and then:

    pip install datuma --pre

# Development
Use virtualenv with Python 3.5 or later.

## Setup
Working in development mode:

    python setup.py develop

## Publish

    python setup.py register
    python setup.py upload
