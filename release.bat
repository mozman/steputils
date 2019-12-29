@ECHO OFF
ECHO Upload to PyPI - NO TEST
PAUSE
twine upload --repository pypi dist/steputils*
mv -f dist/steputils* dist/archive