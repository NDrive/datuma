import time
import inspect
import importlib.util

from .cmd import Server, Container, shell
import datuma.database

DATUMA_DIR="~/.datuma"

def generate_archive_path(config):
    uid = "database-%s-%s" % (config["database"], int(time.time()))
    path = DATUMA_DIR + "/"+ uid + ".tar.gz"
    return path


def dump(config, database, archive, server):
    if "container" in config["source"]:
        container = Container(config["source"]["container"])

    server.ssh("mkdir -p " + DATUMA_DIR)

    cmd = database.dump(
        database=config["source"]["database"],
        user="postgres"
    )

    if "container" in config["source"]:
        cmd = "sudo " + container.execute(cmd)

    cmd += " | gzip > " + archive
    print("[dump] %s" % cmd)
    server.ssh(cmd)


def transfer(config, archive, server):
    shell("mkdir -p " + DATUMA_DIR)
    cmd = "rsync {host}:{archive} {archive}".format(
        host=config["source"]["server"],
        archive=archive)
    print("[transfer] %s" % cmd)
    shell(cmd)
    server.ssh("rm -f " + archive)


def restore(config, database, archive):
    cmd = database.restore(database=config["destination"]["database"])
    if "container" in config["destination"]:
        container = Container(config["destination"]["container"])
        extra_options = "--user=postgres" if config["type"] == "postgres" else ""
        cmd = container.execute(cmd, options="-i %s" % extra_options)

    cmd = "gunzip -c " + archive + " | " + cmd
    print("[restore] %s" % cmd)
    shell(cmd)
    shell("rm -f " + archive)


def validate_schema(config):
    """ Validates presence of keys in restore definition and database type. """
    # Root keys
    expected_keys = {"database", "type", "source", "destination"}
    diff = expected_keys - set(config.keys())
    if diff:
        raise Exception("Missing keys: %s" % diff)

    # Database
    if not importlib.util.find_spec("datuma.database." + config["type"]):
        raise Exception("Invalid database type %s" % config["type"])

    # Source
    expected_keys = {"server", "container", "database"}
    diff = expected_keys - set(config["source"].keys())
    if diff:
        raise Exception("Missing keys in source: %s" % diff)

    # Destination
    expected_keys = {"database"}
    diff = expected_keys - set(config["destination"].keys())
    if diff:
        raise Exception("Missing keys in destination: %s" % diff)


def migrate(config):
    try:
        validate_schema(config)
    except Exception as e:
        raise Exception("Error in %s database restore definition: %s " % (config, e))

    print("======= [%s] =======" % config["database"])

    archive = generate_archive_path(config)
    server = Server(config["source"]["server"])
    database = importlib.import_module("datuma.database." + config["type"])

    dump(config, database, archive, server)
    transfer(config, archive, server)
    restore(config, database, archive)
