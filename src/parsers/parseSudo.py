import re

def parseSudoLine(line):
    date = re.search(r'^[A-Za-z]{3}\s*[0-9]{1,2}\s[0-9]{1,2}:[0-9]{2}:[0-9]{2}', line)
    user = re.search(r'(?<=ruser=).*?(?=\s)', line)
    tty =  re.search(r'(?<=tty=).*?(?=\s)', line)
    if date != None and user != None and tty != None:
        logEntry = "SUDO " + date.group()
        return logEntry, user.group(), tty.group()
    else:
        return line