"""
Script for automatic pause/unpause of F@H worker slots if they fail to download
new WUs, which often fixes that problem faster than simply waiting until enough
attempts have been made.
"""

import subprocess
import time
import re
import itertools
from file_read_backwards import FileReadBackwards


# CONFIGURATION

# define here the path to FAH log file (log.txt)
LOGFILE_PATH = r""

# define here the path to FAH client binary (FAHClient.exe)
FAH_BINARY_PATH = r""


# COMMAND EXECUTION

PAUSE_COMMAND = r"--send-pause"
UNPAUSE_COMMAND = r"--send-unpause"

def fah_execute_command(command):
    """Execute the command, which is a list of arguments, on the FAH client."""
    subprocess.run([FAH_BINARY_PATH] + command, check=True)

def fah_cycle_slot(slot, sleep_time=10):
    """Pause, wait and unpause the slot."""
    fah_execute_command([PAUSE_COMMAND, str(slot)])
    time.sleep(sleep_time)
    fah_execute_command([UNPAUSE_COMMAND, str(slot)])


# LOG PROCESSING

LOG_SLOT_ID_PATTERN = re.compile(r":FS(\d+):")
LOG_WU_FAULT_PATTERN = re.compile(r"No WUs available for this configuration")

def log_get_most_recent_lines(limit):
    """Get lines from the back of the log."""
    lines = []
    with FileReadBackwards(LOGFILE_PATH, encoding="utf-8") as frb:
        for line in itertools.islice(frb, limit):
            lines.append(line)
    return lines[::-1]


def log_get_slot(log_line):
    """Match the slot id from a log line."""
    match = LOG_SLOT_ID_PATTERN.search(log_line)
    if match:
        return match.group(1)
    return None

def log_is_wu_fault(log_line):
    """Determine if the log line indicates failing WU retrieval."""
    if LOG_WU_FAULT_PATTERN.search(log_line):
        return True
    return False


# MAIN SCRIPT

def cycle_faulted():
    """Check if any slot has faulted and if so, cycle it."""
    last_lines = log_get_most_recent_lines(2)
    if any(log_is_wu_fault(line) for line in last_lines):
        slot = log_get_slot(last_lines[-1])
        if slot is not None:
            print("Cycling slot " + str(slot))
            fah_cycle_slot(slot)


if __name__ == "__main__":
    print("Starting")
    while True:
        cycle_faulted()
        time.sleep(30)
