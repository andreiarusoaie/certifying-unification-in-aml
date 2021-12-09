for file in $(pwd)/tests/samples/*.in
do
    python3 ml-unify.py "$file"
done