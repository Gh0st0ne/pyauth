import re

def parseFTPLine(line):
    date = re.search(r'^[A-Za-z]{3}\s*[0-9]{1,2}\s[0-9]{1,2}:[0-9]{2}:[0-9]{2}', line)
    ip = re.search(r'[^rhost=][0-9]+\.[0-9]+\.[0-9]+\.[0-9]+',line)
    if date != None and ip != None:
        logEntry = "FTP " + date.group() + " from " + ip.group() + " port 21"
        return logEntry
    else:
        return line
