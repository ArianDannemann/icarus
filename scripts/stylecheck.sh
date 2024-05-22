echo -:- PEP8 -:-
pycodestyle --ignore=E501,W504,W503 *.py
echo -:- Pylint -:-
pylint *.py
echo -:- MyPy -:-
mypy --strict --disallow-untyped-defs --disallow-incomplete-defs --disallow-any-explicit --disallow-any-generics *.py
