echo -:- PEP8 -:-
pycodestyle *.py
echo -:- Pylint -:-
pylint *.py
echo -:- MyPy -:-
mypy .
