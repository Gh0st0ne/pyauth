import re

def parsePostgresLine(line):
    date = re.search(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}\s[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{1,}', line)
    user = re.search(r'\"(.*?)\"', line)
    if date != None and user != None:
        logEntry = "Postgres " + date.group()
        return logEntry, user.group()
    else:
        return line, None