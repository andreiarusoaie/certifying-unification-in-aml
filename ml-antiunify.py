import sys
from src import utils as u
from src import aunifcert as c

MAUDE = 'maude'

def main():
    u.check_maude_installation(MAUDE);
    c.certify(sys.argv)

main()
