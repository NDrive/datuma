import time
import inspect
import importlib.util
import logging

from .cmd import Server, Container, shell
import datuma.database


DATUMA_DIR = "~/.datuma"


def generate_archive_path(config):
    uid = "database-%s-%s" % (config["database"], int(time.time()))
    path = DATUMA_DIR + "/" + uid + ".tar.gz"
    return path


def dump(config, database, archive, server):
    if "container" in config["source"]:
        container = Container(config["source"]["container"])

    server.ssh("mkdir -p " + DATUMA_DIR)

    cmd = database.dump(**config["source"])

    if "container" in config["source"]:
        cmd = "sudo " + container.execute(cmd)
    else:
        cmd = "sudo " + database.prefix() + " " + cmd

    cmd += " | gzip > " + archive
    logging.info("- Dump: %s" % cmd)
    server.ssh(cmd)


def transfer(config, archive, server):
    shell("mkdir -p " + DATUMA_DIR)
    cmd = "rsync {host}:{archive} {archive}".format(
        host=config["source"]["server"],
        archive=archive)
    logging.info("- Transfer: %s" % cmd)
    shell(cmd)
    server.ssh("rm -f " + archive)


def restore(config, database, archive):
    cmd = database.restore(**config["destination"])

    # If drop=true, recreate an empty database
    if config["destination"].get("drop", False) and not "container" in config["destination"]:
        logging.info("- Dropping and creating empty database")
        shell(database.dropdb(database=config["destination"]["database"]), ignore_errors=True)
        shell(database.createdb(database=config["destination"]["database"]))

    if "container" in config["destination"]:
        container = Container(config["destination"]["container"])
        extra_options = "--user=postgres" if config["type"] == "postgres" else ""
        cmd = container.execute(cmd, options="-i %s" % extra_options)

    cmd = "gunzip -c " + archive + " | " + cmd
    logging.info("- Restore: %s" % cmd)

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
    expected_keys = {"server"}
    diff = expected_keys - set(config["source"].keys())
    if diff:
        raise Exception("Missing keys in source: %s" % diff)


def migrate(config):
    try:
        validate_schema(config)
        logging.debug("Schema is valid")
    except Exception as e:
        raise Exception("Error in %s database restore definition: %s " % (config, e))

    archive = generate_archive_path(config)
    server = Server(config["source"]["server"])
    database = importlib.import_module("datuma.database." + config["type"])

    logging.info("Database %s of type %s" % (config["database"],  config["type"]))
    logging.info("- Archive: %s" % archive)
    logging.info("- Server: %s" % config["source"]["server"])

    dump(config, database, archive, server)
    transfer(config, archive, server)
    restore(config, database, archive)
