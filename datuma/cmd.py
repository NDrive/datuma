import subprocess


def shell(cmd, ignore_errors=False):
    """ Executes commands through shell """
    try:
        return subprocess.check_output(cmd, shell=True)
    except Exception as e:
        if ignore_errors:
            return ""
        else:
            raise e


class Server:
    """ Executes commands through SSH """
    def __init__(self, host):
        self.host = host

    def ssh(self, cmd):
        ssh_cmd = "ssh {host} '{cmd}'".format(host=self.host, cmd=cmd)
        return shell(ssh_cmd)


class Container:
    """ Generates commands for a running container """
    def __init__(self, name):
        self.name = name

    def execute(self, cmd, options=""):
        cmd = "docker exec {options} {container} sh -c \"{cmd}\"".format(options=options, container=self.name, cmd=cmd)
        return cmd
