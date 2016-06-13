import time
import inspect

from .cmd import Server, Container, shell
from .database import postgres

import migrator.database

MIGRATOR_DIR="~/.migrator"

def generate_archive_path(database):
    uid = "database-%s-%s" % (database["database"], int(time.time()))
    path = MIGRATOR_DIR + "/"+ uid + ".tar.gz"
    return path


def dump(database, archive, server):
    server.ssh("mkdir -p " + MIGRATOR_DIR)
    cmd = postgres.dump(
        database=database["source"]["database"],
        user="postgres",
        archive=archive
    )
    if "container" in database["source"]:
        container = Container(database["source"]["container"])
        cmd = "sudo " + container.execute(cmd)
    cmd += " | gzip > " + archive
    print("[dump] %s" % cmd)
    server.ssh(cmd)


def transfer(database, archive, server):
    shell("mkdir -p " + MIGRATOR_DIR)
    cmd = "rsync {host}:{archive} {archive}".format(
        host=database["source"]["server"],
        archive=archive)
    print("[transfer] %s" % cmd)
    shell(cmd)
    server.ssh("rm -f " + archive)


def restore(database, archive):
    cmd = postgres.restore(database=database["database"])
    if "container" in database["destination"]:
        container = Container(database["destination"]["container"])
        cmd = container.execute(cmd, options="-i --user=postgres")
    cmd = "gunzip -c " + archive + " | " + cmd
    print("[restore] %s" % cmd)
    shell(cmd)
    shell("rm -f " + archive)


def validate_schema(database):
    """ Validates presence of keys in restore definition and database type. """
    # Root keys
    expected_keys = {"database", "type", "source", "destination"}
    diff = expected_keys - set(database.keys())
    if diff:
        raise Exception("Missing keys: %s" % diff)

    # Database
    databases = [db[0] for db in inspect.getmembers(migrator.database, inspect.ismodule)]
    if database["type"] not in databases:
        raise Exception("Invalid database type %s" % database["type"])

    # Source
    expected_keys = {"server", "container", "database"}
    diff = expected_keys - set(database["source"].keys())
    if diff:
        raise Exception("Missing keys in source: %s" % diff)

    # Destination
    expected_keys = {"container", "database"}
    diff = expected_keys - set(database["destination"].keys())
    if diff:
        raise Exception("Missing keys in destination: %s" % diff)


def migrate(database):
    try:
        validate_schema(database)
    except Exception as e:
        raise Exception("Error in %s database restore definition: %s " % (database, e))

    print("======= [%s] =======" % database["database"])

    archive = generate_archive_path(database)
    server = Server(database["source"]["server"])

    dump(database, archive, server)
    transfer(database, archive, server)
    restore(database, archive)
