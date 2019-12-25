@ECHO OFF
ECHO TEST TEST TEST - upload to TestPyPI - TEST TEST TEST
twine upload --repository testpypi dist/ifc4data*
mv -f dist/ifc4data* dist/archiv