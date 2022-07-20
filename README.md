# dbET

## Prerequisite
* Install PostgreSQL on your machine. Our experiments are conducted on a Ubuntu 20.04 instance using PostgreSQL 12.9.
* Install Python and Psycopg2, the latter is a library to interact with PostgreSQL using Python.
* Import IMDb dataset. A detailed instruction can be found here: https://github.com/waltercai/pqo-opensource.
* Download the sample workload in `data/JOB-light`.

## Generating calibration samples
The generation of offline training samples is done by `generating_training_data.py`. Before running the function, one needs to set the path to workload (line 8), authorization to the PostgreSQL database (line 10), and the destination  directory of the generated training data (line 14). If the users want to use a subset of hints for training data generation, they can simply do so by adjusting line 63. Run file `generating_training_data.py` and the training data should now be generated and written to the specified destination.

## Calibrating the cost estimator
Calibrating the cost estimator and saving the distribution constructor are done by `calibrate_cost_estimator.py`. Set the path to the training data generated in the last step (line 11), determine the alphas to be used in the experiment (line 14), and specify the directory to save the distribution constructor (line 18). Now run the file, and the constructors should start being generated. One can also adjust training parameters in file `estimator/model.py` such as the number of epochs in line 182.

## Testing the method
Now that we have the distribution constructors, we can testify the method using file `test_method.py`. Set line 10 and line 14 in the file as in the last step. Provide a test query in line 26, choose how many hints to use in line 43, and the execution time distributions of the candidate plans will be printed.

Detailed comments and explanations are also provided inline in each file. The learned cost estimator in this experiment is cloned from https://github.com/learnedsystems/baoforpostgresql (with some midification).
