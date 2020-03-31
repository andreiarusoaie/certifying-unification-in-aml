import shlex
from subprocess import Popen, PIPE
import time
import os

# setup
MAUDE        = 'maude' # modify this with the full path of the maude executable
TESTS        = 'tests' # tests folder
EXPECTED_OUT = 'out'

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
    for test in os.listdir(tests):
        if (test == 'tests-setup.maude' or test == "out"):
            continue
        file = os.path.join(tests, test)
        file_log_out = os.path.join(tests, log_dir,
                                    test.replace('.maude', ".out"))
        print("[TESTING]", file)
        (out, err, ex, tm) = system_call(MAUDE + " -no-banner " + file)
        if (ex == 0):
            out_decoded = out.decode('utf-8')
            n = open(file_log_out, 'wb')
            n.write(out)
            if ('step-marker' in out_decoded):
                print('[FAILURE]', 'proof failed,', 'output saved in ', file_log_out)
            else:
                print('[SEEMS OK]', 'check output saved in ', file_log_out)
        else:
            print('[FAILURE]', err.decode('uft-8'))

def main():
    check_maude_installation();
    run_tests();

main()
