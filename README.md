# Migrator _(in development)_

A tool to automate migrations of data between database instances. It allows you
for example, to automate tests based on real production data.

# Requirements
  - Python 3.5

# Database support
 - Postgres in Docker containers
 - Rethinkdb in Docker containers

# Usage

Syntax:

```
usage: migrate [-h] [--file FILE] [database [database ...]]

Tool to migrate databases between instances.

positional arguments:
 database              List of databases, otherwise all

optional arguments:
 -h, --help            show this help message and exit
 --file FILE, -f FILE  JSON file path with the restores configuration
```

Create a `migrator.json` to create restores definitions:

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

    migrate

Run only data migration of one database:

    migrate products

# Install
Meanwhile the tool is in development, install it from Github:

    pip install git+https://github.com/NDrive/migrator
