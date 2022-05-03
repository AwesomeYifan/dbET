from os import listdir
from os.path import isfile, join
import statistics
import random
import psycopg2
from estimator.model import *

# step 2:train and calibrate the learned estimator

# set the following variables:
path_to_training_plans = "data/JOB-light/postgres_plans"
# the path to the training plans generated in the last step

alphas = [0.1,0.2,0.3]
# related to the conformal technique
# each alpha correspondes to a model

model_dir = "model/"
# the calibrated models will be saved here

# code begins here
def load_training_data():
    X, y = [], []
    files = [f for f in listdir(path_to_training_plans) if isfile(join(path_to_training_plans, f))]
    for fname in files:
        read_path = join(path_to_training_plans, fname)
        if not isfile(read_path):
            continue
        try:
            f = open(read_path, 'r')
            for line in f.readlines():
                plan = json.loads(line)[0]
                X.append(plan)
                t = float(plan['Execution Time'])
                y.append(t)
        except:
            print(f)
    return X, y

# train
plans, runtimes = load_training_data() 
for alpha in alphas:
    model = BaoRegression(verbose=True, alpha=alpha)
    model.fit(plans,runtimes)
    model.save(model_dir +'/' + str(alpha) + '/')