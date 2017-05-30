def dump(**kwargs):
    return "cat {rdb}".format(**kwargs)


def restore(**kwargs):
    cmd = "cat > dump.rdb; rdb --command protocol dump.rdb | nc {address} {port} ; rm dump.rdb"
    return cmd.format(**kwargs)


def prefix():
    return ""
