def dump(**kwargs):
    if "password" in kwargs:
        return "echo '{password}' > password.txt; rethinkdb dump --export {database} --file temp.tar.gz --password-file password.txt > /dev/null; cat temp.tar.gz; rm temp.tar.gz password.txt > /dev/null".format(**kwargs)
    else:
        return "rethinkdb dump --export {database} --file temp.tar.gz > /dev/null; cat temp.tar.gz; rm temp.tar.gz > /dev/null".format(**kwargs)

def restore(**kwargs):
    defaults = {
        "options": ""
    }
    return "cat > temp.tar.gz; rethinkdb restore {options} temp.tar.gz ; rm temp.tar.gz".format(**{**defaults, **kwargs})

def prefix():
    return ""

def drop():
    return ""
