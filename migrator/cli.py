""" CLI main entrypoint. """

import argparse
import json

from migrator.migrator import migrate


def parse():
    parser = argparse.ArgumentParser(description='Tool to migrate databases between instances.')
    parser.add_argument('--file', '-f', help='JSON file path with the restores configuration', default="migrator.json")
    parser.add_argument('--database', '-d', help='Restores a specific database, otherwise all')
    args = parser.parse_args()
    return args


def parse_config(file_path):
    f = open(file_path, "r")
    config = json.loads(f.read())
    f.close()
    return config


def filter_databases(config, args):
    if args.database:
        databases = [c for c in config if c["database"] == args.database]
    else:
        databases = config
    return databases


def main():
    args = parse()
    config = parse_config(args.file)
    databases = filter_databases(config, args)
    [migrate(d) for d in databases]

if __name__ == '__main__':
    main()
