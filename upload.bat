@ECHO OFF
ECHO TEST TEST TEST - upload to TestPyPI - TEST TEST TEST
twine upload --repository testpypi dist/steputils*
mv -f dist/steputils* dist/archiv