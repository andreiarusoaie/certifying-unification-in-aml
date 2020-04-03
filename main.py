import shlex
from subprocess import Popen, PIPE
import time
import os

# setup
MAUDE        = 'maude' # modify this with the full path of the maude executable
TESTS        = 'tests' # tests folder
EXPECTED_OUT = 'out'   # the outputs are saved in the out folder under TESTS

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


def check_maude_installation():
    (out, err, exit_code, elapsed_time) = system_call(MAUDE + " --version");
    if (exit_code == 0):
        print("Found Maude version:", out.decode('utf-8'))
    else:
        print("Maude not found:", err)

def run_tests():
    dir = os.path.dirname(os.path.realpath(__file__))
    tests = os.path.join(dir, TESTS)
    log_dir = os.path.join(tests, EXPECTED_OUT)
    passed = 0
    failed = 0
    failed_list = []
    for test in os.listdir(tests):
        if (test == 'tests-setup.maude' or test == "out"):
            continue
        file = os.path.join(tests, test)
        file_log_out = os.path.join(tests, log_dir,
                                    test.replace('.maude', ".out"))
        print(BOLD + "[TESTING]" + ENDC, file)
        (out, err, ex, tm) = system_call(MAUDE + " -no-banner " + file)
        if (ex == 0):
            out_decoded = out.decode('utf-8')
            n = open(file_log_out, 'wb')
            n.write(out)
            if ('step-marker' in out_decoded):
                print(FAIL + '[FAILURE]' + ENDC, 'proof failed, output saved in ',
                      file_log_out)
                failed = failed + 1
                failed_list.append(test)
            else:
                print(OKGREEN + '[OK]' + ENDC, 'check output saved in ',
                      file_log_out)
                passed = passed + 1
        else:
            print(WARNING + '[MAUDE FAILURE]' + ENDC, err.decode('uft-8'))
            failed = failed + 1
            failed_list.append(test)
    print(BOLD + HEADER + "[TOTAL TESTS]:", passed + failed, ENDC)
    print(OKGREEN + "[PASSED]:", passed, ENDC)
    print(FAIL + "[FAILED]:", failed, ENDC)
    if (failed > 0):
        print(BOLD + FAIL + "[FAILED TESTS]:", failed_list, ENDC)

def main():
    check_maude_installation();
    run_tests();

main()
