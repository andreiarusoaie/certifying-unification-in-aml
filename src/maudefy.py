from src import term

def to_aml(t1, t2):
    (maude_t1, encoding, available_key) = term_to_aml(t1, {}, 1);
    (maude_t2, encoding, available_key) = term_to_aml(t2, encoding, available_key)
    return (maude_t1, maude_t2, encoding)

SYMB = "\\symb"
EVAR = "\\evar"

def get_maude_term(prec, tag, encoding, available_key):
    if not (tag in encoding.keys()):
        encoding[tag] = available_key
        available_key = available_key + 1
    return (prec + "(" + str(encoding[tag]) + ")",  encoding, available_key)

def get_rec_app(trm, sub_terms):
    if not sub_terms:
        print("error: get_rec_app called with", trm, sub_terms)
        exit(4);
    n = len(sub_terms)
    if n == 1:
        return "\\app(" + trm + ", " + sub_terms[0] + ")"
    return "\\app(" + get_rec_app(trm, sub_terms[:n-1]) + ", " + sub_terms[n-1] + ")"


def sorts_list(n):
  return ('TermPattern ' * n).strip()

def term_to_aml(t, encoding, available_key):
    if t.isConstant():
        return get_maude_term(SYMB, t.tag, encoding, available_key)
    elif t.isVar():
        return get_maude_term(EVAR, t.tag, encoding, available_key)
    else:
        (maude_tag, s_enc, s_key) = get_maude_term(SYMB, t.tag, encoding, available_key)
        sterms = []
        for subterm in t.subterms:
            (s_t, s_enc, s_key) = term_to_aml(subterm, s_enc, s_key)
            sterms.append(s_t)
        return (get_rec_app(maude_tag, sterms), s_enc, s_key)

def get_ops(arities, variables):
    ops = []
    for (op, ar) in arities.items():
        ops.append('op ' + op + ' : ' +
                   sorts_list(ar) +
                   ' -> TermPattern .')
    for var in variables:
        ops.append('op ' + var + ' : -> EVar .')
    return ops


def T(i):
    return 'T' + str(i)

def get_variables(n):
    vars = []
    for i in range(1, n + 1):
        vars.append(T(i))
    return vars

def get_pretty_eqs(arities, encodings, term_variables):
    max_ar = 0
    eqs = []
    for (op, ar) in arities.items():
        if (max_ar < ar):
            max_ar = ar
        if ar == 0:
            eqs.append('eq prettyTermPattern(\\symb(' + str(encodings[op])
                  + ')) = ' + op + ' .')
        else:
            variables = get_variables(ar)
            apps = get_rec_app('\\symb(' + str(encodings[op]) + ')', variables)
            p_vars = map(lambda x: 'prettyTermPattern(' + x + ')', variables)
            args = ','.join(list(p_vars))
            eqs.append('eq prettyTermPattern(' + apps + ') = ' +
                       op + '(' + args +  ') .')

    for var in term_variables:
        eqs.append('eq prettyTermPattern(\\evar(' + str(encodings[var]) + ')) = ' + var + ' .')

    var_decl = ''
    if (max_ar > 0):
        var_decl = 'vars ' + ' '.join(get_variables(max_ar)) + ' : TermPattern .'


    return [var_decl] + eqs
