import re

def parseSSHLine(line):
    date = re.search(r'^[A-Za-z]{3}\s*[0-9]{1,2}\s[0-9]{1,2}:[0-9]{2}:[0-9]{2}', line)
    ip = re.search(r'(\bfrom\s)(\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b)', line)
    port = re.search(r'\bport\s[0-9]{1,}',line)
    if date != None and ip != None and port != None:
        logEntry = "SSH " + date.group() + " " + ip.group() + " " + port.group() 
        return logEntry
    else:
        return line