import yaml
import os
import time
import re
import sys
from parsers import parseSSH, parseFTP, parsePostgres, parseSudo
from threading import Thread
import helpers


# We are monitoring the given file contionusly in here.
def monitorTheFile(logFile):
    logFile.seek(0, 2)
    while True:
        line = logFile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


def analyzeLogs(logFileName, **type):
    with open(logFileName, 'r') as logFile:
        logLines = monitorTheFile(logFile)
        if type.get("key1") == "SSH" or type.get("key2") == "FTP" or type.get("key3") == "SUDO":
            for line in logLines:
                if re.findall(helpers.regexForSSHFail, line):
                    logEntry = parseSSH.parseSSHLine(line)
                    print(helpers.bcolors.FAIL + "[FAILED] " + helpers.bcolors.ENDC + "%s" % logEntry.strip())
                elif re.findall(helpers.regexForSSHAccept, line):
                    logEntry = parseSSH.parseSSHLine(line)
                    print(helpers.bcolors.OKGREEN + "[ACCEPTED] " + helpers.bcolors.ENDC + "%s" % logEntry.strip())
                elif re.findall(helpers.regexForFTPFail, line):
                    logEntry = parseFTP.parseFTPLine(line)
                    print(helpers.bcolors.FAIL + "[FAILED] " + helpers.bcolors.ENDC + "%s" % logEntry.strip())
                elif re.findall(helpers.regexForSudoFail, line):
                    logEntry, user, tty = parseSudo.parseSudoLine(line)
                    print(helpers.bcolors.FAIL + "[FAILED] " + helpers.bcolors.ENDC + "%s failed login attempt for user=%s and tty=%s" % (logEntry.strip(), user, tty))
        elif type.get("key1") == "Postgres":
            for line in logLines:
                if re.findall(helpers.regexForPostgresFail, line):
                    logEntry, user = parsePostgres.parsePostgresLine(line)
                    print(
                        helpers.bcolors.FAIL + "[FAILED] " + helpers.bcolors.ENDC + "%s failed login attempt for %s" % (
                            logEntry.strip(), user))


def isExist(fileName):
    if os.path.isfile(fileName):
        return True


# We're using threads to monitor seperate files simultaneously
def startMonitoring(distribution):
    with open("fileList.yaml", 'r') as stream:
        try:
            yamlData = yaml.safe_load(stream)
            if isExist(yamlData[distribution]["auth"]):
                Thread(target=analyzeLogs, args=(yamlData[distribution]["auth"],),
                       kwargs={'key1': "SSH", 'key2': "FTP", 'key3': "SUDO"}).start()
            if isExist(yamlData[distribution]["postgres"]):
                Thread(target=analyzeLogs, args=(yamlData[distribution]["postgres"],),
                       kwargs={'key1': "Postgres"}).start()
        except yaml.YAMLError as exc:
            print(exc)


def main():
    # We are staring our critical function in here
    distribution = ""
    with open("distro.yaml", 'r') as distroStream:
        try:
            distroYaml = yaml.safe_load(distroStream)
            if distroYaml["distro"]["debian"] or distroYaml["distro"]["ubuntu"]:
                distribution = "debian"
            elif distroYaml["distro"]["centos"]:
                distribution = "centos"
        except yaml.YAMLError as exc:
            print(exc)

    startMonitoring(distribution)


if __name__ == "__main__":
    try:
        sys.path.append('./')
        main()
    except Exception as e:
        print(e, "\n" + ' bay...')
