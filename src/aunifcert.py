import os
import sys
import re
from . import parser
from . import maudefy as m
from . import utils as u

MAUDE    = 'maude'
TEMPLATE = 'auniftemplate.maude'
TEMP     = 'auniflog.maude'

def get_file_as_string(filename):
    try:
        file = open(filename, 'r')
        return file.read()
    except FileNotFoundError as e:
        u.err(str(e))

def search(tag, term):
    rest = set()
    if (tag == term.tag):
        ar = int(len(term.subterms))
        rest.add(ar)
    for subterm in term.subterms:
        rest = set.union(rest, search(tag, subterm))
    return rest

def check_variables(vars, t1, t2):
    for var in vars:
        if not search(var, t1) and not search(var, t2):
            u.err("variable", var, "is not used")

def check_symbols(symbols, t1, t2):
    for symbol in symbols:
        if not search(symbol, t1) and not search(symbol, t2):
            u.err("symbol", symbol, "is not used")

def get_arity_map(symbols, t1, t2):
    symb_arity = {}
    for symbol in symbols:
        o1 = list(search(symbol, t1))
        o2 = list(search(symbol, t2))
        if (len(o1) == 0 and len(o2) == 0):
            u.err("cannot determine arity of symbol", symbol,
                  "from your list of symbols", symbols)
        if len(o1) > 1 or len(o2) > 1:
            u.err("ambiguous arity of symbol", symbol, "in", t1, t2)
        if len(o1) == 1 and len(o2) == 1 and o1[0] != o2[0]:
            u.err("ambiguous arity of symbol", symbol, "in", t1, t2)
        if len(o1) == 1:
            symb_arity[symbol] = o1[0]
        if len(o2) == 1:
            symb_arity[symbol] = o2[0]
    return symb_arity

def my_escape(s):
    return s.replace('\\a', '\\\\a').replace('\s', '\\\s').replace('\\e', '\\\\e')

def generate_maude(t1, t2, symbols, variables, dir):
    # generate maude internal represenation for terms
    (maude_t1, maude_t2, encoding_map) = m.to_aml(t1, t2)

    # generate maude module for proof generation and pretty printing
    arities = get_arity_map(symbols, t1, t2)
    ops = m.get_ops(arities, variables)
    eqs = m.get_pretty_eqs(arities, encoding_map, variables)
    ops_string = '\n    '.join(ops)
    eqs_string = my_escape('\n    '.join(eqs))
    dir = os.path.dirname(os.path.realpath(__file__))
    template = os.path.join(dir, TEMPLATE)
    template_text = get_file_as_string(template)
    template_text = re.sub(r"DECLARATIONS", ops_string,
                           template_text, flags=re.MULTILINE)
    template_text = re.sub(r"PRETTYPRINT", eqs_string,
                           template_text, flags=re.MULTILINE)
    template_text = re.sub(r"TERM1", my_escape(maude_t1), template_text)
    template_text = re.sub(r"TERM2", my_escape(maude_t2), template_text)
    return template_text

def flagcolor(s):
    if (str(s).strip() == 'true'):
        return u.BOLD + u.OKGREEN + s + u.ENDC
    else:
        return u.BOLD + u.FAIL + s + u.ENDC

def get_goal(proofline):
    regex_pl = re.compile(r'\([0-9]+\)([^\[]*)\[.*\]')
    match = regex_pl.match(proofline)
    if match:
        return match.group(1)
    else:
        return "cannot extract proof goal; the goal is the last line in this proof"

def extract_maude(out):
    regex_prf = re.compile(r'Proof:(.*?)(====|Bye)', re.DOTALL)
    regex_chk = re.compile(r'Bool:(.*?)(====|Bye)', re.DOTALL)
    output = out.decode("utf-8")
    proofs = [p.groups() for p in regex_prf.finditer(output)]
    checks = [c.groups() for c in regex_chk.finditer(output)]
    if len(proofs) != 1 or len(checks) != 1:
        print("cannot extract proofs and checks from maude output")
        print("please run `maude", log,'`` to find out what is wrong')
        exit(1)
    i = 1
    for proof in proofs:
        lastline = proof[0].strip().splitlines()[-1];
        print(u.BOLD + u.HEADER + "Proof of:" + u.OKBLUE, get_goal(lastline), u.ENDC)
        print(proof[0].strip())
        print(u.OKBLUE + "Checked:", u.ENDC, flagcolor(checks[i - 1][0]))
        i = i + 1


def certify(args):
    # handle input args
    if (len(args) <= 1):
        u.err("Please provide an input file")

    # parse input file
    input_filename = args[1];
    input = get_file_as_string(input_filename)
    (variables, symbols, t1, t2) = parser.parse(input)
    check_variables(variables, t1, t2)
    check_symbols(symbols, t1, t2)

    dir = os.path.dirname(os.path.realpath(__file__))
    template_text = generate_maude(t1, t2, symbols, variables, dir)
    log           = os.path.join(dir, TEMP)

    # save the generated maude module and execute maude
    maude_temp = open(log, 'w')
    maude_temp.write(template_text)
    maude_temp.close()
    (out, er, ex, vtime) = u.system_call(MAUDE + " " + log +
                                         " -no-advise -no-banner -no-wrap")

    # extract maude output
    if ex == 0:
        extract_maude(out)
    else:
        u.err("cannot execute", MAUDE, "\nERROR")
