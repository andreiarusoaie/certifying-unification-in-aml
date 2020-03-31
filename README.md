# certifying-unification-in-aml
This repo contains a series of Maude scripts for generating and checking proof certificates for syntactic unification in (Applicative) Matching Logic.

### Prerequisites

> Software 
  * We recommend [Python 3](https://www.python.org/downloads/) needed to execute `main.py`; Python 2.7 also works, but the output looks a bit odd.
  * The proof checker and the proof generator are written in [Maude 3](http://maude.cs.illinois.edu/w/index.php/Maude_download_and_installation).

> Literature
  * [Unifcation in Matching Logic](https://link.springer.com/chapter/10.1007/978-3-030-30942-8_30)
  * [Applicative Matching Logic](http://fsl.cs.illinois.edu/index.php/Applicative_Matching_Logic)

### Guidelines
The `main.py` script (Python 3) checks if `Maude` is installed and runs automatically all the tests. If the `maude` executable is not available in PATH then you can update `main.py` to look into a different location.

The `src` folder contains a proof checker for (Applicative) Matching Logic in `checker.maude` and a proof generator for syntactc unification in `proof-generator.maude`.

The `tests` folder contains a setup file `tests-setup.maude` and a list of files `n_some_description.maude` where `n` is the test number and `some_description` is a short description indicating the name of the tested rules. Each file generates and checks two proofs for a particular unification problem that is written as a comment at the beginning of the file.

### Scripts usage

Open a terminal, `cd` into your working dir and type:

```
-$ git clone https://github.com/andreiarusoaie/certifying-unification-in-aml.git
-$ cd certifying-unification-in-aml
-$ make
```
This will run all the tests in the `tests` folder. Initally, all tests pass. If you want to add more tests in the `tests` directory, please follow the same naming convention as in the **Guidelines** section above. You can inspect the output in the corresponding file in the `tests/out/` directory.

### Using the checker

#### (Applicative) Matching Logic formulas
The syntax of the formulas is given below:

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
The proof generator provides two functions `gen-proof1` and `gen-proof2` that are used to generate proofs for the unification of two *term patterns* `t1` and `t2` given as arguments. 

Let us consider two term patterns `f(x)` and `f(y)` encoded as `\app(\symb(1), \evar(1))` and `\app(\symb(1), \evar(2))`. The following Maude commands generate proofs for the unification problem `f(x) =? f(y)`:

```
rew in PROOF-GENERATION : gen-proof1(\app(\symb(1), \evar(1)), \app(\symb(1), \evar(2))) .
rew in PROOF-GENERATION : gen-proof2(\app(\symb(1), \evar(1)), \app(\symb(1), \evar(2))) .
```

#### Using the proof checker

The above commands will generate two proofs. We can check them by simply calling `check` as follows:

```
rew in PROOF-GENERATION : check(gen-proof1(\app(\symb(1), \evar(1)), \app(\symb(1), \evar(2)))) .
rew in PROOF-GENERATION : check(gen-proof2(\app(\symb(1), \evar(1)), \app(\symb(1), \evar(2)))) .
```

If `check` returns `true`, then the proof was checked successfully. Otherwise, the proof is displayed together with a coloured marker that indicates where the proof checking failed.

### Contact
You can contact me at andrei . arusoaie at uaic ro.
