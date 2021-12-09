# Samples 

This folder contains several samples, from small trivial examples up to larger examples inspired from real-life K language definitions (C and Java). 
Each sample `*.in` can be passed as an input to our main scripts like this:

* for unification: `python3 ml-unify.py tests/samples/<sample>.in`
* for anti-unification: `python3 ml-antiunify.py tests/samples/<sample>.in`

When `python3 ml-antiunify.py tests/samples/<sample>.in` is executed on an input sample, the Python script displays the corresponding proof-object. 

The table below shows the results that correspond to some of our most interesting tests. 
On each line we find the input file name and its size, the proof-object size (expressed as the number of proof lines for both unification and anti-unification. 
Since our proof-object generation depends on the number of steps performed by the algorithms, we expects the size of the proof-objects to be linear w.r.t. to these steps. Also, we use the file size (in kb) to give a measure of how big are the term patterns in that particular test.

| File name  | File size (kb) | Unification | Antiunification | 
|------------|----------------|-------------|-----------------|
| `13_paper_cons_succ.in` | 0.122 | 43 | 84 |
| `16_simple_untyped_lookup.in` | 1.3 | 312 | 804 |
| `17_simple_untyped_release_lock.in` | 1.3 | 272  | 768 |
| `18_c_declare_local.in` | 14 | 2006 | 5052 |
| `19_java_method_invoke.in` | 6 | 933 | 2352 |

The size of the inputs which are inspired by the C and Java configurations (i.e., the inputs are actually symbolic K configurations from the C and Java semantics).  We can see that the size of the proof-object generated for C is almost twice when compared with the proof-object generated for the Java example. This is because the configuration of the C language is 2 times larger than the configuration of Java.


The outputs for each sample are stored in this repo as well:
* [here](https://github.com/andreiarusoaie/certifying-unification-in-aml/tree/master/tests/samples/outputs/unification) are the outputs for unification
* [here](https://github.com/andreiarusoaie/certifying-unification-in-aml/tree/master/tests/samples/outputs/anti-unification) are the outputs for anti-unification
