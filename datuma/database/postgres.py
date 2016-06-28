def dump(**kwargs):
    return "pg_dump --user {user} {database}".format(**kwargs)


def restore(**kwargs):
    return "psql {database}".format(**kwargs)

def prefix():
    return "-u postgres"
