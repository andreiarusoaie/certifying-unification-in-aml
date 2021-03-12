# Certifying (anti)unification in Matching Logic
This repo contains a series of Maude scripts for generating and checking proof certificates for syntactic unification and anti-unification in (Applicative) Matching Logic.

## Overview
* [Prerequisites](#prerequisites)
* [Repo organisation](#repo-organisation)
* [Setup](#setup)
* [Scripts](#scripts)
* [Using the Maude scripts directly](#using-the-maude-scripts-directly)

### Prerequisites

> Software 
  * We recommend [Python 3](https://www.python.org/downloads/) needed to execute `ml-unify.py`; Python 2.7 also works, but the output looks a bit odd.
  * The proof checker and the proof generator are written in [Maude 3](http://maude.cs.illinois.edu/w/index.php/Maude_download_and_installation).

> Literature
  * [Unification in Matching Logic](https://link.springer.com/chapter/10.1007/978-3-030-30942-8_30)
  * [Applicative Matching Logic](http://fsl.cs.illinois.edu/index.php/Applicative_Matching_Logic)

### Repo Organisation
The `ml-unify.py` script (Python 3) checks if `Maude` is installed and processes an input file with a specific format. This is explained in detail in the subsection **ml-unify.py** below.

The `tests.py` script (Python 3) checks if `Maude` is installed and runs automatically all the tests.

The `src` folder contains a proof checker for (Applicative) Matching Logic in `checker.maude` and a proof generator for syntactic unification in `proof-generator.maude`. 

The `tests\maude` folder contains a setup file `tests-setup.maude` and a list of files `n_some_description.maude` where `n` is the test number and `some_description` is a short description indicating the name of the tested rules. Each file generates and checks two proofs for a particular unification problem that is written as a comment at the beginning of the file.

## Setup

Open a terminal, `cd` into your working dir and type:

```
-$ git clone https://github.com/andreiarusoaie/certifying-unification-in-aml.git
-$ cd certifying-unification-in-aml
-$ make
```
This will run all the tests in the `tests\maude` folder. Initally, all tests pass. If you want to add more tests in the `tests\maude` directory, please follow the same naming convention as in the **Guidelines** section above. You can inspect the output in the corresponding file in the `tests/out/` directory.

## Scripts
### ml-unify.py

The `ml-unify.py` script takes as input files that specify unification problems. Here's an example:

```
variables: x, z
symbols: f, g , u, t
problem: f(x, g(z, x)) =? f(x, g(u, t))
```

The `variables:` and `symbols:` sections contain the syntax to be used for terms. `problem:` is the unification problem to be solved. `ml-unify.py` parses this content and calls Maude which:
  * solves the unification problem,
  * generates a proof in (Applicative) Matching Logic, and
  * checks the generated proof (and thus, it outputs a proof certificate).

If the above specification is in `problem.in`, then `ml-unify.py` is invoked like this:

```
-$ python3 ml-unify.py problem.in 
Found Maude version: 3.0beta1

Proof of: (f(x, g(u, t)) and f(x, g(z, x)) --> f(x, g(z, x)) and (x === t) and (z === u))
(1)((f(x, g(z, x)) === f(x, g(u, t))) --> (f(x, g(z, x)) === f(x, g(u, t)))) [tauto-imp-refl] ;
(2)((f(x, g(z, x)) === f(x, g(u, t))) --> (x === x) and (g(z, x) === g(u, t))) [axiom-no-confusion-II] ;
(3)((f(x, g(z, x)) === f(x, g(u, t))) --> (x === x) and (g(z, x) === g(u, t))) [tauto-imp-tranz,1,2] ;
(4)((g(z, x) === g(u, t)) --> (x === t) and (z === u)) [axiom-no-confusion-II] ;
(5)((x === x) and (g(z, x) === g(u, t)) --> (x === t) and (x === x) and (z === u)) [tauto-context,4] ;
(6)((f(x, g(z, x)) === f(x, g(u, t))) --> (x === t) and (x === x) and (z === u)) [tauto-imp-tranz,3,5] ;
(7)((x === x) --> (ff --> ff)) [tauto-equality-id] ;
(8)((x === t) and (x === x) and (z === u) --> (ff --> ff) and (x === t) and (z === u)) [tauto-context,7] ;
(9)((ff --> ff) and (x === t) and (z === u) --> (x === t) and (z === u)) [tauto-and-unit] ;
(10)((x === t) and (x === x) and (z === u) --> (x === t) and (z === u)) [tauto-imp-tranz,8,9] ;
(11)((f(x, g(z, x)) === f(x, g(u, t))) --> (x === t) and (z === u)) [tauto-imp-tranz,6,10] ;
(12)(f(x, g(z, x)) and (f(x, g(z, x)) === f(x, g(u, t))) --> f(x, g(z, x)) and (x === t) and (z === u)) [tauto-context,11] ;
(13)(f(x, g(u, t)) and f(x, g(z, x)) --> f(x, g(z, x)) and (f(x, g(z, x)) === f(x, g(u, t)))) [axiom-5.24.3-1] ;
(14)(f(x, g(u, t)) and f(x, g(z, x)) --> f(x, g(z, x)) and (x === t) and (z === u)) [tauto-imp-tranz,13,12] ;
Checked:   true

Proof of: (f(x, g(z, x)) and (x === t) and (z === u) --> f(x, g(u, t)) and f(x, g(z, x)))
(1)((x === t) and (z === u) --> (x === t) and (z === u)) [tauto-imp-refl] ;
(2)((ff --> ff) --> (x === x)) [tauto-equality-refl] ;
(3)((ff --> ff) and (x === t) and (z === u) --> (x === t) and (x === x) and (z === u)) [tauto-context,2] ;
(4)((x === t) and (z === u) --> (ff --> ff) and (x === t) and (z === u)) [tauto-and-exp-unit] ;
(5)((x === t) and (z === u) --> (x === t) and (x === x) and (z === u)) [tauto-imp-tranz,4,3] ;
(6)((x === t) and (z === u) --> (x === t) and (x === x) and (z === u)) [tauto-imp-tranz,1,5] ;
(7)((x === t) and (z === u) --> (g(z, x) === g(u, t))) [axiom-functional] ;
(8)((x === t) and (x === x) and (z === u) --> (x === x) and (g(z, x) === g(u, t))) [tauto-context,7] ;
(9)((x === t) and (z === u) --> (x === x) and (g(z, x) === g(u, t))) [tauto-imp-tranz,6,8] ;
(10)((x === x) and (g(z, x) === g(u, t)) --> (f(x, g(z, x)) === f(x, g(u, t)))) [axiom-functional] ;
(11)((x === t) and (z === u) --> (f(x, g(z, x)) === f(x, g(u, t)))) [tauto-imp-tranz,9,10] ;
(12)(f(x, g(z, x)) and (x === t) and (z === u) --> f(x, g(z, x)) and (f(x, g(z, x)) === f(x, g(u, t)))) [tauto-context,11] ;
(13)(f(x, g(z, x)) and (f(x, g(z, x)) === f(x, g(u, t))) --> f(x, g(u, t)) and f(x, g(z, x))) [axiom-5.24.3-2] ;
(14)(f(x, g(z, x)) and (x === t) and (z === u) --> f(x, g(u, t)) and f(x, g(z, x))) [tauto-imp-tranz,12,13] ;
Checked:   true
```

The output contains two proofs (one for each stage - check [Unification in Matching Logic](https://link.springer.com/chapter/10.1007/978-3-030-30942-8_30) for details). If the `Checked` flags are both `true` then the proofs have been checked successfully.

`ml-unify.py` can also throw errors if the input is not correct. For instance:

> Example 1: a declared variable is not used
```
-$ cat err_not_used.in
variables: x, z
symbols: f, g , k, u, t
problem: f =? f(x, g(u, t))
-$ python3 ml-unify.py err_not_used.in
Found Maude version: 3.0beta1

ERROR: variable z is not used 
Exit with non-zero code: 1
```

> Example 2: a symbol is used with different arities
```
-$ cat err_ambiguous_arity.in
variables: x
symbols: f, g , k, u, t
problem: f =? f(x, g(u, t))
-$ python3 ml-unify.py err_ambiguous_arity.in
Found Maude version: 3.0beta1

ERROR: ambiguous arity of symbol f in f f(x,g(u,t)) 
Exit with non-zero code: 1
```

> Example 3: a term is not well-formed
```
-$ cat err_parsing_bad_term.in
variables: x, z
symbols: f, g , k, u, t
problem: f(x)x) =? f(x, g(u, t))
-$ python3 ml-unify.py err_parsing_bad_term.in
Found Maude version: 3.0beta1

ERROR: cannot parse f(x)x), stopped here x) 
Exit with non-zero code: 4
```


> Example 4: a variable is used instead of a symbol
```
-$ cat err_parsing_bad_symb.in
variables: x, z
symbols: f, g , k, u, t
problem: x(x) =? f(x, g(u, t))
-$ python3 ml-unify.py err_parsing_bad_symb.in
Found Maude version: 3.0beta1

ERROR: bad symbol x, expecting one of ['f', 'g', 'k', 'u', 't'] 
Exit with non-zero code: 4
```

### ml-antiunify.py
This script is very similar to `ml-unify.py`, except it produces a proof that corresponds to anti-unification of terms. The input has the same format:

```
variables: x, z
symbols: f, g , u, t
problem: f(x, g(z, x)) =? f(x, g(u, t))
```

On this input, the produces proof is:

```
$ python3 ml-antiunify.py tests/samples/1_dec.in 
Found Maude version: 3.0

Proof of: (f(x, g(u, t)) or f(x, g(z, x)) <--> ∃ v(8) ; v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and f(v(8), g(v(10), v(11))))  
(1)(f(x, g(z, x)) <--> ∃ v(5) . v(5) and (v(5) === f(x, g(z, x)))) [sbst1] ;

(2)(f(x, g(u, t)) <--> ∃ v(5) . v(5) and (v(5) === f(x, g(u, t)))) [sbst1] ;

(3)(f(x, g(u, t)) or f(x, g(z, x)) <--> (∃ v(5) . v(5) and (v(5) === f(x, g(u, t)))) or (∃ v(5) . v(5) and (v(5) === f(x, g(z, x))))) [eqv-or(1, 2)] ;

(4)((∃ v(5) . v(5) and (v(5) === f(x, g(u, t)))) or (∃ v(5) . v(5) and (v(5) === f(x, g(z, x)))) <--> ∃ v(5) . v(5) and (v(5) === f(x, g(u, t))) or v(5) and (v(5) === f(x, g(z, x)))) [e-collapse] ;

(5)(v(5) and ((v(5) === f(x, g(u, t))) or (v(5) === f(x, g(z, x)))) <--> v(5) and (v(5) === f(x, g(u, t))) or v(5) and (v(5) === f(x, g(z, x)))) [and-or-distr] ;

(6)((∃ v(5) . v(5) and ((v(5) === f(x, g(u, t))) or (v(5) === f(x, g(z, x))))) <--> ∃ v(5) . v(5) and (v(5) === f(x, g(u, t))) or v(5) and (v(5) === f(x, g(z, x)))) [e-intro(5)] ;

(7)(f(x, g(u, t)) or f(x, g(z, x)) <--> ∃ v(5) . v(5) and (v(5) === f(x, g(u, t))) or v(5) and (v(5) === f(x, g(z, x)))) [eqv-tranz(3, 4)] ;

(8)(f(x, g(u, t)) or f(x, g(z, x)) <--> ∃ v(5) . v(5) and ((v(5) === f(x, g(u, t))) or (v(5) === f(x, g(z, x))))) [eqv-tranz(7, 6)] ;

(9)((v(5) === f(x, g(z, x))) <--> ∃ v(8) ; v(9) . (v(5) === f(v(8), v(9))) and (v(8) === x) and (v(9) === g(z, x))) [e-gen] ;

(10)((v(5) === f(x, g(z, x))) <--> ∃ v(8) ; v(9) . (v(5) === f(v(8), v(9))) and (v(8) === x) and (v(9) === g(z, x))) [and-eqv-intro(9)] ;

(11)((∃ v(8) ; v(9) . (v(5) === f(v(8), v(9))) and (v(8) === x) and (v(9) === g(z, x))) <--> ∃ v(8) ; v(9) . (v(5) === f(v(8), v(9))) and (v(8) === x) and (v(9) === g(z, x))) [e-scope] ;

(12)((v(5) === f(x, g(z, x))) <--> ∃ v(8) ; v(9) . (v(5) === f(v(8), v(9))) and (v(8) === x) and (v(9) === g(z, x))) [eqv-tranz(10, 11)] ;

(13)((v(5) === f(x, g(u, t))) <--> ∃ v(8) ; v(9) . (v(5) === f(v(8), v(9))) and (v(8) === x) and (v(9) === g(u, t))) [e-gen] ;

(14)((v(5) === f(x, g(u, t))) <--> ∃ v(8) ; v(9) . (v(5) === f(v(8), v(9))) and (v(8) === x) and (v(9) === g(u, t))) [and-eqv-intro(13)] ;

(15)((∃ v(8) ; v(9) . (v(5) === f(v(8), v(9))) and (v(8) === x) and (v(9) === g(u, t))) <--> ∃ v(8) ; v(9) . (v(5) === f(v(8), v(9))) and (v(8) === x) and (v(9) === g(u, t))) [e-scope] ;

(16)((v(5) === f(x, g(u, t))) <--> ∃ v(8) ; v(9) . (v(5) === f(v(8), v(9))) and (v(8) === x) and (v(9) === g(u, t))) [eqv-tranz(14, 15)] ;

(17)((v(5) === f(x, g(u, t))) or (v(5) === f(x, g(z, x))) <--> (∃ v(8) ; v(9) . (v(5) === f(v(8), v(9))) and (v(8) === x) and (v(9) === g(u, t))) or (∃ v(8) ; v(9) . (v(5) === f(v(8), v(9))) and (v(8) === x) and (v(9) === g(z, x)))) [eqv-or(12, 16)] ;

(18)((∃ v(8) ; v(9) . (v(5) === f(v(8), v(9))) and (v(8) === x) and (v(9) === g(u, t))) or (∃ v(8) ; v(9) . (v(5) === f(v(8), v(9))) and (v(8) === x) and (v(9) === g(z, x))) <--> ∃ v(8) ; v(9) . (v(5) === f(v(8), v(9))) and (v(8) === x) and (v(9) === g(u, t)) or (v(5) === f(v(8), v(9))) and (v(8) === x) and (v(9) === g(z, x))) [e-collapse] ;

(19)((v(5) === f(x, g(u, t))) or (v(5) === f(x, g(z, x))) <--> ∃ v(8) ; v(9) . (v(5) === f(v(8), v(9))) and (v(8) === x) and (v(9) === g(u, t)) or (v(5) === f(v(8), v(9))) and (v(8) === x) and (v(9) === g(z, x))) [eqv-tranz(17, 18)] ;

(20)(((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (v(5) === f(v(8), v(9))) <--> (v(5) === f(v(8), v(9))) and (v(8) === x) and (v(9) === g(u, t)) or (v(5) === f(v(8), v(9))) and (v(8) === x) and (v(9) === g(z, x))) [and-or-distr] ;

(21)((∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (v(5) === f(v(8), v(9)))) <--> ∃ v(8) ; v(9) . (v(5) === f(v(8), v(9))) and (v(8) === x) and (v(9) === g(u, t)) or (v(5) === f(v(8), v(9))) and (v(8) === x) and (v(9) === g(z, x))) [e-intro(20)] ;

(22)((v(5) === f(x, g(u, t))) or (v(5) === f(x, g(z, x))) <--> ∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (v(5) === f(v(8), v(9)))) [eqv-tranz(19, 21)] ;

(23)((∃ v(5) . v(5) and ((v(5) === f(x, g(u, t))) or (v(5) === f(x, g(z, x))))) <--> ∃ v(5) . v(5) and (∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (v(5) === f(v(8), v(9))))) [e-context(22)] ;

(24)(v(5) and (∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (v(5) === f(v(8), v(9)))) <--> ∃ v(8) ; v(9) . v(5) and ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (v(5) === f(v(8), v(9)))) [e-scope] ;

(25)((∃ v(5) . v(5) and (∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (v(5) === f(v(8), v(9))))) <--> ∃ v(5) . ∃ v(8) ; v(9) . v(5) and ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (v(5) === f(v(8), v(9)))) [e-intro(24)] ;

(26)((∃ v(5) . ∃ v(8) ; v(9) . v(5) and ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (v(5) === f(v(8), v(9)))) <--> ∃ v(5) ; v(8) ; v(9) . v(5) and ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (v(5) === f(v(8), v(9)))) [e-set] ;

(27)((∃ v(5) . v(5) and (∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (v(5) === f(v(8), v(9))))) <--> ∃ v(5) ; v(8) ; v(9) . v(5) and ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (v(5) === f(v(8), v(9)))) [eqv-tranz(25, 26)] ;

(28)(((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (∃ v(5) . v(5) and (v(5) === f(v(8), v(9)))) <--> ∃ v(5) . v(5) and ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (v(5) === f(v(8), v(9)))) [e-scope] ;

(29)((∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (∃ v(5) . v(5) and (v(5) === f(v(8), v(9))))) <--> ∃ v(8) ; v(9) . ∃ v(5) . v(5) and ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (v(5) === f(v(8), v(9)))) [e-intro(28)] ;

(30)((∃ v(8) ; v(9) . ∃ v(5) . v(5) and ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (v(5) === f(v(8), v(9)))) <--> ∃ v(5) ; v(8) ; v(9) . v(5) and ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (v(5) === f(v(8), v(9)))) [e-set] ;

(31)((∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (∃ v(5) . v(5) and (v(5) === f(v(8), v(9))))) <--> ∃ v(5) ; v(8) ; v(9) . v(5) and ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (v(5) === f(v(8), v(9)))) [eqv-tranz(30, 29)] ;

(32)(f(v(8), v(9)) <--> ∃ v(5) . v(5) and (v(5) === f(v(8), v(9)))) [sbst1] ;

(33)((∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and f(v(8), v(9))) <--> ∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (∃ v(5) . v(5) and (v(5) === f(v(8), v(9))))) [e-context(32)] ;

(34)((∃ .Vars . ∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and f(v(8), v(9))) <--> ∃ .Vars . ∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (∃ v(5) . v(5) and (v(5) === f(v(8), v(9))))) [e-intro(33)] ;

(35)((∃ .Vars . ∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (∃ v(5) . v(5) and (v(5) === f(v(8), v(9))))) <--> ∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (∃ v(5) . v(5) and (v(5) === f(v(8), v(9))))) [e-set] ;

(36)((∃ .Vars . ∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and f(v(8), v(9))) <--> ∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and f(v(8), v(9))) [e-set] ;

(37)((∃ .Vars . ∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and f(v(8), v(9))) <--> ∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (∃ v(5) . v(5) and (v(5) === f(v(8), v(9))))) [eqv-tranz(35, 34)] ;

(38)((∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and f(v(8), v(9))) <--> ∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (∃ v(5) . v(5) and (v(5) === f(v(8), v(9))))) [eqv-tranz(37, 36)] ;

(39)((∃ v(5) . v(5) and ((v(5) === f(x, g(u, t))) or (v(5) === f(x, g(z, x))))) <--> ∃ v(5) ; v(8) ; v(9) . v(5) and ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (v(5) === f(v(8), v(9)))) [eqv-tranz(23, 27)] ;

(40)((∃ v(5) . v(5) and ((v(5) === f(x, g(u, t))) or (v(5) === f(x, g(z, x))))) <--> ∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and (∃ v(5) . v(5) and (v(5) === f(v(8), v(9))))) [eqv-tranz(39, 31)] ;

(42)((∃ v(5) . v(5) and ((v(5) === f(x, g(u, t))) or (v(5) === f(x, g(z, x))))) <--> ∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and f(v(8), v(9))) [eqv-tranz(38, 40)] ;

(43)(f(x, g(u, t)) or f(x, g(z, x)) <--> ∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and f(v(8), v(9))) [eqv-tranz(8, 42)] ;

(44)((v(9) === g(z, x)) <--> ∃ v(10) ; v(11) . (v(9) === g(v(10), v(11))) and (v(10) === z) and (v(11) === x)) [e-gen] ;

(45)((v(8) === x) and (v(9) === g(z, x)) <--> (v(8) === x) and (∃ v(10) ; v(11) . (v(9) === g(v(10), v(11))) and (v(10) === z) and (v(11) === x))) [and-eqv-intro(44)] ;

(46)((v(8) === x) and (∃ v(10) ; v(11) . (v(9) === g(v(10), v(11))) and (v(10) === z) and (v(11) === x)) <--> ∃ v(10) ; v(11) . (v(8) === x) and (v(9) === g(v(10), v(11))) and (v(10) === z) and (v(11) === x)) [e-scope] ;

(47)((v(8) === x) and (v(9) === g(z, x)) <--> ∃ v(10) ; v(11) . (v(8) === x) and (v(9) === g(v(10), v(11))) and (v(10) === z) and (v(11) === x)) [eqv-tranz(45, 46)] ;

(48)((v(9) === g(u, t)) <--> ∃ v(10) ; v(11) . (v(9) === g(v(10), v(11))) and (v(10) === u) and (v(11) === t)) [e-gen] ;

(49)((v(8) === x) and (v(9) === g(u, t)) <--> (v(8) === x) and (∃ v(10) ; v(11) . (v(9) === g(v(10), v(11))) and (v(10) === u) and (v(11) === t))) [and-eqv-intro(48)] ;

(50)((v(8) === x) and (∃ v(10) ; v(11) . (v(9) === g(v(10), v(11))) and (v(10) === u) and (v(11) === t)) <--> ∃ v(10) ; v(11) . (v(8) === x) and (v(9) === g(v(10), v(11))) and (v(10) === u) and (v(11) === t)) [e-scope] ;

(51)((v(8) === x) and (v(9) === g(u, t)) <--> ∃ v(10) ; v(11) . (v(8) === x) and (v(9) === g(v(10), v(11))) and (v(10) === u) and (v(11) === t)) [eqv-tranz(49, 50)] ;

(52)((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x)) <--> (∃ v(10) ; v(11) . (v(8) === x) and (v(9) === g(v(10), v(11))) and (v(10) === u) and (v(11) === t)) or (∃ v(10) ; v(11) . (v(8) === x) and (v(9) === g(v(10), v(11))) and (v(10) === z) and (v(11) === x))) [eqv-or(47, 51)] ;

(53)((∃ v(10) ; v(11) . (v(8) === x) and (v(9) === g(v(10), v(11))) and (v(10) === u) and (v(11) === t)) or (∃ v(10) ; v(11) . (v(8) === x) and (v(9) === g(v(10), v(11))) and (v(10) === z) and (v(11) === x)) <--> ∃ v(10) ; v(11) . (v(8) === x) and (v(9) === g(v(10), v(11))) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(9) === g(v(10), v(11))) and (v(10) === z) and (v(11) === x)) [e-collapse] ;

(54)((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x)) <--> ∃ v(10) ; v(11) . (v(8) === x) and (v(9) === g(v(10), v(11))) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(9) === g(v(10), v(11))) and (v(10) === z) and (v(11) === x)) [eqv-tranz(52, 53)] ;

(55)(((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and (v(9) === g(v(10), v(11))) <--> (v(8) === x) and (v(9) === g(v(10), v(11))) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(9) === g(v(10), v(11))) and (v(10) === z) and (v(11) === x)) [and-or-distr] ;

(56)((∃ v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and (v(9) === g(v(10), v(11)))) <--> ∃ v(10) ; v(11) . (v(8) === x) and (v(9) === g(v(10), v(11))) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(9) === g(v(10), v(11))) and (v(10) === z) and (v(11) === x)) [e-intro(55)] ;

(57)((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x)) <--> ∃ v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and (v(9) === g(v(10), v(11)))) [eqv-tranz(54, 56)] ;

(58)((∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and f(v(8), v(9))) <--> ∃ v(8) ; v(9) . f(v(8), v(9)) and (∃ v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and (v(9) === g(v(10), v(11))))) [e-context(57)] ;

(59)(f(v(8), v(9)) and (∃ v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and (v(9) === g(v(10), v(11)))) <--> ∃ v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and f(v(8), v(9)) and (v(9) === g(v(10), v(11)))) [e-scope] ;

(60)((∃ v(8) ; v(9) . f(v(8), v(9)) and (∃ v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and (v(9) === g(v(10), v(11))))) <--> ∃ v(8) ; v(9) . ∃ v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and f(v(8), v(9)) and (v(9) === g(v(10), v(11)))) [e-intro(59)] ;

(61)((∃ v(8) ; v(9) . ∃ v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and f(v(8), v(9)) and (v(9) === g(v(10), v(11)))) <--> ∃ v(8) ; v(9) ; v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and f(v(8), v(9)) and (v(9) === g(v(10), v(11)))) [e-set] ;

(62)((∃ v(8) ; v(9) . f(v(8), v(9)) and (∃ v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and (v(9) === g(v(10), v(11))))) <--> ∃ v(8) ; v(9) ; v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and f(v(8), v(9)) and (v(9) === g(v(10), v(11)))) [eqv-tranz(60, 61)] ;

(63)(((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and (∃ v(9) . f(v(8), v(9)) and (v(9) === g(v(10), v(11)))) <--> ∃ v(9) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and f(v(8), v(9)) and (v(9) === g(v(10), v(11)))) [e-scope] ;

(64)((∃ v(8) ; v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and (∃ v(9) . f(v(8), v(9)) and (v(9) === g(v(10), v(11))))) <--> ∃ v(8) ; v(10) ; v(11) . ∃ v(9) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and f(v(8), v(9)) and (v(9) === g(v(10), v(11)))) [e-intro(63)] ;

(65)((∃ v(8) ; v(10) ; v(11) . ∃ v(9) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and f(v(8), v(9)) and (v(9) === g(v(10), v(11)))) <--> ∃ v(8) ; v(9) ; v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and f(v(8), v(9)) and (v(9) === g(v(10), v(11)))) [e-set] ;

(66)((∃ v(8) ; v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and (∃ v(9) . f(v(8), v(9)) and (v(9) === g(v(10), v(11))))) <--> ∃ v(8) ; v(9) ; v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and f(v(8), v(9)) and (v(9) === g(v(10), v(11)))) [eqv-tranz(65, 64)] ;

(67)(f(v(8), g(v(10), v(11))) <--> ∃ v(9) . f(v(8), v(9)) and (v(9) === g(v(10), v(11)))) [sbst1] ;

(68)((∃ v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and f(v(8), g(v(10), v(11)))) <--> ∃ v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and (∃ v(9) . f(v(8), v(9)) and (v(9) === g(v(10), v(11))))) [e-context(67)] ;

(69)((∃ v(8) . ∃ v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and f(v(8), g(v(10), v(11)))) <--> ∃ v(8) . ∃ v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and (∃ v(9) . f(v(8), v(9)) and (v(9) === g(v(10), v(11))))) [e-intro(68)] ;

(70)((∃ v(8) . ∃ v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and (∃ v(9) . f(v(8), v(9)) and (v(9) === g(v(10), v(11))))) <--> ∃ v(8) ; v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and (∃ v(9) . f(v(8), v(9)) and (v(9) === g(v(10), v(11))))) [e-set] ;

(71)((∃ v(8) . ∃ v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and f(v(8), g(v(10), v(11)))) <--> ∃ v(8) ; v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and f(v(8), g(v(10), v(11)))) [e-set] ;

(72)((∃ v(8) . ∃ v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and f(v(8), g(v(10), v(11)))) <--> ∃ v(8) ; v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and (∃ v(9) . f(v(8), v(9)) and (v(9) === g(v(10), v(11))))) [eqv-tranz(70, 69)] ;

(73)((∃ v(8) ; v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and f(v(8), g(v(10), v(11)))) <--> ∃ v(8) ; v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and (∃ v(9) . f(v(8), v(9)) and (v(9) === g(v(10), v(11))))) [eqv-tranz(72, 71)] ;

(74)((∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and f(v(8), v(9))) <--> ∃ v(8) ; v(9) ; v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and f(v(8), v(9)) and (v(9) === g(v(10), v(11)))) [eqv-tranz(58, 62)] ;

(75)((∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and f(v(8), v(9))) <--> ∃ v(8) ; v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and (∃ v(9) . f(v(8), v(9)) and (v(9) === g(v(10), v(11))))) [eqv-tranz(74, 66)] ;

(77)((∃ v(8) ; v(9) . ((v(8) === x) and (v(9) === g(u, t)) or (v(8) === x) and (v(9) === g(z, x))) and f(v(8), v(9))) <--> ∃ v(8) ; v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and f(v(8), g(v(10), v(11)))) [eqv-tranz(73, 75)] ;

(78)(f(x, g(u, t)) or f(x, g(z, x)) <--> ∃ v(8) ; v(10) ; v(11) . ((v(8) === x) and (v(10) === u) and (v(11) === t) or (v(8) === x) and (v(10) === z) and (v(11) === x)) and f(v(8), g(v(10), v(11)))) [eqv-tranz(43, 77)] ;
Checked:   true

```

The output contains a single proof of the equivalence <img src="https://render.githubusercontent.com/render/math?math=t_1 \vee t_2 \leftrightarrow \exists\overline{z}.t\wedge(\phi^{\sigma_1} \vee \phi^{\sigma_2})">.

## Using the Maude scripts directly 

### (Applicative) Matching Logic formulas
The syntax of the formulas (file `checker.maude`) is given below:

```
subsort EVar < TermPattern .
op \evar : NzNat                    -> EVar .
op \symb : NzNat                    -> TermPattern .
op \app  : TermPattern TermPattern  -> TermPattern .
op \imp  : TermPattern TermPattern  -> TermPattern .
op \bot  :                          -> TermPattern .
```

For convenience, we add some derived syntax:
```
    op _and_ : TermPattern TermPattern -> TermPattern [assoc comm prec 30] .
    op \not  : TermPattern             -> TermPattern .
    op \eq   : TermPattern TermPattern -> TermPattern .
```

With this syntax we build formulas:

* `\evar(1)` - represents a variable;
* `\symb(1)` - represents a constant symbol;
* `\app(\symb(1), \evar(1))` - represents an application. The `\app` constructor is used to build *term patterns*. We can think of `\app(\symb(1), \evar(1))` as `f(x)`, where `f` is `\symb(1)` and `x` is `\evar(1)`;
* `\imp(\eq(\app(\symb(1), \evar(1)), \app(\symb(1), \evar(2))), \eq(\evar(1), \evar(2))` is a *pattern*. If we use `y` to denote `\evar(2)` then our pattern is `f(x) = f(y) -> x = y`.

#### Using the proof generator

There are two proof generators: `proof-generator.maude` for unification and `aunif-proof-generator.maude` for antiunification.

The `proof-generator.maude` provides two functions `gen-proof1` and `gen-proof2` that are used to generate proofs for the unification of two *term patterns* `t1` and `t2` given as arguments. 

Let us consider two term patterns `f(x)` and `f(y)` encoded as `\app(\symb(1), \evar(1))` and `\app(\symb(1), \evar(2))`. The following Maude commands generate proofs for the unification problem `f(x) =? f(y)`:

```
rew in PROOF-GENERATION : gen-proof1(\app(\symb(1), \evar(1)), \app(\symb(1), \evar(2))) .
rew in PROOF-GENERATION : gen-proof2(\app(\symb(1), \evar(1)), \app(\symb(1), \evar(2))) .
```

The `aunif-proof-generator.maude` provides only one function `gen-proof` for generating the only proof needed. Continuing the above example, this ca be used as follows:

```
rew in PROOF-GENERATION : gen-proof(\app(\symb(1), \evar(1)), \app(\symb(1), \evar(2))) .
```

#### Using the proof checker in Maude

The above commands will generate two proofs. We can check them by simply calling `check` as follows:

> For unification:
```
rew in PROOF-GENERATION : check(gen-proof1(\app(\symb(1), \evar(1)), \app(\symb(1), \evar(2)))) .
rew in PROOF-GENERATION : check(gen-proof2(\app(\symb(1), \evar(1)), \app(\symb(1), \evar(2)))) .
```

> For antiunification:
```
rew in PROOF-GENERATION : check(gen-proof(\app(\symb(1), \evar(1)), \app(\symb(1), \evar(2)))) .
```


If `check` returns `true`, then the proof was checked successfully. Otherwise, the proof is displayed together with a coloured marker that indicates where the proof checking failed.

### Contact
You can contact me at andrei . arusoaie at uaic ro.
