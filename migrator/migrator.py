import time
from .cmd import Server, Container, shell
from .database import postgres

MIGRATOR_DIR="~/.migrator"

def generate_archive_uid(database):
    return "database-%s-%s" % (database["database"], int(time.time()))

def migrate(database):
    archive = MIGRATOR_DIR + generate_archive_uid(database) + ".tar.gz"
    server = Server(database["source"]["server"])
    container = Container(database["source"]["container"])

    # Dump
    server.ssh("mkdir -p " + MIGRATOR_DIR)
    postgres_cmd = postgres.dump(
        database=database["source"]["database"],
        user="postgres",
        archive=archive
    )
    server.ssh("sudo " + container.execute(postgres_cmd))

    # Transfer
    shell("mkdir -p " + MIGRATOR_DIR)
    shell("rsync {host}:{archive} {archive}".format(
        host=database["source"]["server"],
        archive=archive))
    server.ssh("rm -f " + archive)
