import shlex
from subprocess import Popen, PIPE
import time
import os
from src import utils as u

# setup
MAUDE        = 'maude'       # modify this with the full path of the maude executable
TESTS        = 'tests'       # tests folder
DIR          = 'unification' # unification tests
EXPECTED_OUT = 'out'         # the outputs are saved in the out folder under DIR


def run_tests():
    dir = os.path.dirname(os.path.realpath(__file__))
    tests = os.path.join(dir, TESTS, DIR)
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
        print(u.BOLD + "[TESTING]" + u.ENDC, file)
        (out, err, ex, tm) = u.system_call(MAUDE + " -no-banner " + file)
        if (ex == 0):
            out_decoded = out.decode('utf-8')
            n = open(file_log_out, 'wb')
            n.write(out)
            if ('step-marker' in out_decoded):
                print(u.FAIL + '[FAILURE]' + u.ENDC, 'proof failed, output saved in ',
                      file_log_out)
                failed = failed + 1
                failed_list.append(test)
            else:
                print(u.OKGREEN + '[OK]' + u.ENDC, 'check output saved in ',
                      file_log_out)
                passed = passed + 1
        else:
            print(u.WARNING + '[MAUDE FAILURE]' + u.ENDC, err.decode('uft-8'))
            failed = failed + 1
            failed_list.append(test)
    print(u.BOLD + u.HEADER + "[TOTAL TESTS]:", passed + failed, u.ENDC)
    print(u.OKGREEN + "[PASSED]:", passed, u.ENDC)
    print(u.FAIL + "[FAILED]:", failed, u.ENDC)
    if (failed > 0):
        print(u.BOLD + u.FAIL + "[FAILED TESTS]:", failed_list, u.ENDC)

def main():
    u.check_maude_installation(MAUDE);
    run_tests();

main()
