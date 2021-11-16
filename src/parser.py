import sys
import re
from . import term
from . import utils as u

EXIT_NO_INPUT = 1
EXIT_NO_VARS  = 2
EXIT_NO_SYMB  = 3
EXIT_PARSE    = 4

def parse(input):
    variables = get_variables(input)
    symbols = get_symbols(input)
    (t1, t2) = get_terms(input, variables, symbols)
    return (variables, symbols, t1, t2)

def get_variables(input):
    search = re.search(r"variables:(.*?)(?=\n)", input);
    if search:
        return list(map(lambda x : x.strip(), search.group(1).split(',')))
    else:
        u.err("no variables found; please declare them", EXIT_NO_VARS);


def get_symbols(input):
    search = re.search(r"symbols:(.*?)(?=\n)", input);
    if search:
        return list(map(lambda x : x.strip(), search.group(1).split(',')))
    else:
        u.err("no symbols found; please declare them", EXIT_NO_SYMB);

def get_terms(input, vars, symbols):
    search = re.search(r"problem:(.+)=\?(.+)", input, re.DOTALL)
    if search:
        t1 = search.group(1).strip()
        t2 = search.group(2).strip()
        t1 = "".join(t1.split())
        t2 = "".join(t2.split())
        (term1, rest1) = parse_term(t1, vars, symbols)
        if (rest1 != ''):
            parse_err("cannot parse " + t1 + ", stopped here " + rest1)
        (term2, rest2) = parse_term(t2, vars, symbols)
        if (rest2 != ''):
            parse_err("cannot parse " + t2 + ", stopped here " + rest2)
        return(term1, term2)
    return (None, None)

def parse_err(message):
    u.err(message, exit_code = EXIT_PARSE);

def parse_constant_or_var(t_string, vars, symbols):
    if (t_string in vars):
        return term.Term(t_string, [], True)
    elif (t_string in symbols):
        return term.Term(t_string, [])
    else:
        parse_err("expecting constant or variable but found " + t_string)


def find_pos_of_first_delim(t_string):
    separators = [',', '(', ')']
    indices = (list(map(lambda sep : t_string.find(sep), separators)))
    indices.append(len(t_string))
    return min(filter(lambda x : x >= 0, indices))


def parse_term_list(t_string, vars, symbols):
    t_string = t_string.lstrip()
    if (not t_string):
        return ([], '')
    if (t_string[0] == ','):
        t_string = t_string[1:]
    if (t_string[0] == ')'):
        return ([], t_string[1:])
    (trm, rest)     = parse_term(t_string, vars, symbols)
    (subterms, rem) = parse_term_list(rest, vars, symbols)
    return ([trm] + subterms, rem)

def parse_term(t_string, vars, symbols):
    if (not t_string):
        parse_err("expected term but found empty string")
    first = find_pos_of_first_delim(t_string)
    tag  = t_string[:first].strip()
    rest = t_string[first:].strip()
    if (not tag):
        parse_err("expected term but found " + t_string)
    if (not rest):
        return (parse_constant_or_var(tag, vars, symbols), '')
    if (rest[0] == '('):
        (subterms, rem) = parse_term_list(rest[1:], vars, symbols)
        if (tag in symbols):
            return (term.Term(tag, subterms), rem)
        else:
            parse_err("bad symbol " + tag + ", expecting one of " + str(symbols))
    elif (rest[0] == ','):
        return (parse_constant_or_var(tag, vars, symbols), rest[1:])
    elif (rest[0] == ')'):
        return (parse_constant_or_var(tag, vars, symbols), rest)
    else:
        parse_err("expecting term but found " + t_string)
