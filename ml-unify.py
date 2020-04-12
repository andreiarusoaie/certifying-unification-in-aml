import sys
from src import utils as u
from src import cert

MAUDE = 'maude'

def main():
    u.check_maude_installation(MAUDE);
    cert.certify(sys.argv)

main()
