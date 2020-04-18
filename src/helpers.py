import re

regexForSSHFail = re.compile("sshd.*failed", re.IGNORECASE)
regexForSSHAccept = re.compile("sshd.*accepted password", re.IGNORECASE)
regexForPostgresFail = re.compile("fatal:.*password.*failed", re.IGNORECASE)
regexForFTPFail = re.compile("vsftpd:.*authentication failure", re.IGNORECASE)
regexForSudoFail = re.compile("sudo:auth.*failure", re.IGNORECASE)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'