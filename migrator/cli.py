""" CLI main entrypoint. """

import argparse
import json
import sys

from migrator.migrator import migrate


def parse():
    parser = argparse.ArgumentParser(description='Tool to migrate databases between instances.')
    parser.add_argument('--file', '-f', help='JSON file path with the restores configuration', default="migrator.json")
    parser.add_argument('databases', help='List of databases, otherwise all', type=str, nargs='*', metavar='database')
    args = parser.parse_args()
    return args


def parse_config(file_path):
    f = open(file_path, "r")
    try:
        config = json.loads(f.read())
    except:
        raise Exception("File is not valid JSON!")
    finally:
        f.close()

    if len(config) == 0:
        raise Exception("The file doesn't have any migration definitions")

    return config


def filter_config(config, args):
    if args.databases:
        filtered_config = [c for c in config if c["database"] in args.databases]
    else:
        filtered_config = config
    return filtered_config


def main():
    try:
        args = parse()
        config = parse_config(args.file)
        config = filter_config(config, args)
        [migrate(c) for c in config]
    except Exception as e:
        sys.stderr.write("ERROR: %s\n" % e)
        sys.exit(1)


if __name__ == '__main__':
    main()
