cleanWorkspace:
	rm __* -rf



outputClean: s3fpOutputClean adversarialOutputClean migrationOutputClean
	rm -f null_out

s3fpOutputClean:
	rm -f outputs/*s3fp_out

adversarialOutputClean:
	rm -f outputs/*adversarial_out

migrationOutputClean:
	rm -f outputs/*migration_out




logClean: adversarialLogClean migrationLogClean s3fpLogClean condensedLogClean
	rm -f logs/*.csv

s3fpLogClean:
	rm -f logs/*s3fp*

adversarialLogClean:
	rm -f logs/AdversarialTestingResults.csv

migrationLogClean:
	rm -f logs/MigrationTestingResults.csv

condensedLogClean:
	rm -f logs/condensed*





migrationInputClean:
	rm -rf inputs/testInputs/testMigrationInputs/*
	
s3fpClean:
	rm -rf spFunDrivers/s3fpDrivers/*_class

s3fpInputClean:
	rm -f inputs/s3fpInputs/*~s3fpInput*
	rm -f logs/s3fpInputLog.csv

driversClean: s3fpClean
	rm -rf spFunDrivers/*.c spFunDrivers/*.so spFunDrivers/*.py spFunDrivers/__*

reset: cleanWorkspace driversClean outputClean migrationInputClean  logClean s3fpInputClean
