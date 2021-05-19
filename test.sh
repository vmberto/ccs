coverage run -m --omit="tests/*" unittest discover -s ./tests -p '*_test.py' -vv
coverage report -m