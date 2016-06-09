""" Postgres implementation """


def dump(**kwargs):
    return "pg_dump --user {user} {database} | gzip > {archive}".format(**kwargs)


def restore(**kwargs):
    return "gunzip -c {archive} | psql {database}"
