make reset

cd ./AutoRNP/experiments
python repairGSL.py

cd ../../fp-diff-testing

python3 extractor.py mpmath /usr/local/lib/python3.6/dist-packages/mpmath/tests/
python3 extractor.py scipy /usr/local/lib/python3.6/dist-packages/scipy/special/tests/
python3 extractor.py gsl /usr/local/lib/gsl/specfunc/

python3 driverGenerator.py mpmath python
python3 driverGenerator.py scipy python
python3 driverGenerator.py gsl c

python3 classify.py

python3 ../utils/generateSpecialValueInputs.py

python3 diffTester.py