for file in $(pwd)/tests/samples/*.in
do
    python3 ml-antiunify.py "$file"
done
