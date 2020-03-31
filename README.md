# certifying-unification-in-aml
This repo contains a series of Maude scripts for generating and checking proof certificates for syntactic unification in (Applicative) Matching Logic.

### Prerequisites
* We recommend [Python 3](https://www.python.org/downloads/) needed to execute `main.py`; Python 2.7 also works, but the output looks a bit odd.
* [Maude 3](http://maude.cs.illinois.edu/w/index.php/Maude_download_and_installation) is needed to load the Maude files in `src` and `tests`.

### Guidelines
The `main.py` script (Python 3) checks if `Maude` is installed and runs automatically all the tests. 

The `src` folder contains a proof checker for (Applicative) Matching Logic in `checker.maude` and a proof generator for syntactc unification in `proof-generator.maude`.

The `tests` folder contains a setup file `tests-setup.maude` and a list of files `n_some_description.maude`. Each file generates and checks two proofs for a particular unification problem.

### Usage

Open a terminal, `cd` into your working dir and type:

```
-$ git clone https://github.com/andreiarusoaie/certifying-unification-in-aml.git
-$ cd certifying-unification-in-aml
-$ make
```

### Contact
You can contact me at andrei . arusoaie at uaic ro.
