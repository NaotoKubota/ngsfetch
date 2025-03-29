# Modules used in shiba.py and scshiba.py
import subprocess
import logging
logger = logging.getLogger(__name__)

def execute_command(command, log_file=None):
    if log_file:
        with open(log_file, "a") as log:
            result = subprocess.run(command, shell=False, stdout=log, stderr=log)
    else:
        result = subprocess.run(command, shell=False)
    return result.returncode
