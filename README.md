# Migrator _(in development)_

A tool to automate migrations of data between database instances. It allows you
for example, to automate tests based on real production data.

# Requirements
  - Python 3.X

# Database support
 - Postgres in Docker Containers

# Usage

Syntax:
```bash
migrate -h                                                                                
usage: migrate [-h] [--file FILE] [--database DATABASE]

Tool to migrate databases between instances.

optional arguments:
  -h, --help            show this help message and exit
  --file FILE, -f FILE  JSON file path with the restores configuration
  --database DATABASE, -d DATABASE
                        Restores a specific database, otherwise all
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
    "type": "postgres",
    "source": {"server": "db1.company.com", "container": "authentication_postgres_1", "database": "auth"},
    "destination": { "container": "test_authentication_postgres_1", "database": "auth"}
  }
]
```

Run with the `migrate` command:

    migrate

# Install
Meanwhile the tool is in development, install it from Github:

    pip install git+https://github.com/NDrive/migrator
