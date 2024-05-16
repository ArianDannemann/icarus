echo -:- PEP8 -:-
pycodestyle --ignore=E501,W504,W503 *.py
echo -:- Pylint -:-
pylint *.py
echo -:- MyPy -:-
mypy .
