def dump(**kwargs):
    return "rethinkdb dump --export {database} --file temp.tar.gz > /dev/null; cat temp.tar.gz; rm temp.tar.gz > /dev/null".format(**kwargs)


def restore(**kwargs):
    return "cat > temp.tar.gz; rethinkdb restore temp.tar.gz ; rm temp.tar.gz".format(**kwargs)

def prefix():
    return ""
