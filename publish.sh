rm -rf dist/* && 
python setup.py bdist_wheel && 
python -m twine upload -u __token__ -p pypi-AgENdGVzdC5weXBpLm9yZwIkYTAyYzM5OTAtZjg1Yy00OGU5LWFiM2UtNjE0ZmIxY2VjZDllAAIleyJwZXJtaXNzaW9ucyI6ICJ1c2VyIiwgInZlcnNpb24iOiAxfQAABiArxoxZLtggKwRa42gQYLQ4va0sXc9VlcXQJRL1JF1m1Q --repository testpypi dist/*