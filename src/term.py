class Term:

    def __init__(self, tag, subterms, is_var=False):
        self.tag      = tag
        self.subterms = subterms
        self.is_var   = is_var

    def __repr__(self):
        sep = ","
        if (self.subterms):
            subterms = sep.join(map(lambda s : str(s), self.subterms))
            return self.tag + "(" + subterms + ")"
        else:
            return self.tag

    def isConstant(self):
        return self.subterms == [] and not self.is_var

    def isVar(self):
        return self.is_var

    def size(self):
        if self.is_var:
            return 1
        if self.subterms:
            return 1 + sum(list(map(lambda x : x.size(),self.subterms)))
        return 1

    def height(self):
        if self.is_var:
            return 1
        if self.subterms:
            return 1 + max(list(map(lambda x : x.height(),self.subterms)))
        return 1
