@ECHO OFF
ECHO Upload to PyPI - NO TEST
PAUSE
twine upload --repository pypi dist/ifc4data*
mv -f dist/ifc4data* dist/archiv