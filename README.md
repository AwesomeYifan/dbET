# dbET
Our experiments mainly involve the following steps:

* Step 1, generate calibration samples with generating_training_data.py;
* Step 2, calibrate the cost estimator with calibrate_cost_estimator.py
* Step 3, test the method with test_method.py.

Detailed comments are provided inline in each file. We provide a sample workload together with the queries and plans in folder `data/JOB-light` for the reader to try the method. Please follow the above three steps and the detailed comments to run the code. The learned cost estimator in this experiment is cloned from https://github.com/learnedsystems/baoforpostgresql (with some midification).