def dump(**kwargs):
    return "pg_dump --user postgres {database}".format(**kwargs)


def restore(**kwargs):
    return "psql {database}".format(**kwargs)


def prefix():
    return "-u postgres"


def dropdb(**kwargs):
    return "dropdb {database}".format(**kwargs)


def createdb(**kwargs):
    return "createdb {database}".format(**kwargs)
