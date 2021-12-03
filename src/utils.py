import shlex
from subprocess import Popen, PIPE
import time

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'


# simply run a system command and return the needed info
def system_call(cmd, dir=".", verbose=False):
    if (verbose):
        print("[CMD]:", cmd)
    vtime = time.time();
    try:
        process = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE, cwd=dir)
        (output, err) = process.communicate()
        exit_code = process.wait()
        if (exit_code == 0 and verbose):
            print("[DONE]", "\n")
        else:
            if (verbose):
                print("[FAILED]:", err.decode("utf-8"))
                print("[EXIT CODE]:", exit_code)
        if (verbose):
            print("[OUTPUT]:", output.decode("utf-8"))
        vtime = round(time.time() - vtime, 3);
        return (output, err, exit_code, vtime)
    except FileNotFoundError as not_found:
        vtime = round(time.time() - vtime, 3);
        return ('', not_found, 1, vtime);


def check_maude_installation(MAUDE):
    (out, err, exit_code, elapsed_time) = system_call(MAUDE + " --version");
    if (exit_code != 0):
        print("Maude not found:", err)

def err(*messages, exit_code = 1):
    print(FAIL + "ERROR:", ENDC, end="")
    for m in messages:
        print(m, end=" ")
    print("\n" + WARNING + "Exit with non-zero code: " + str(exit_code) + ENDC)
    exit(exit_code)
