import psycopg2
import json
from estimator.model import *
from utils import *

# step 3: produce execution time distribution for new queries/plans

# set the following variables:

alphas = [0.1,0.2,0.3]
# related to the conformal technique
# each alpha correspondes to a model

model_dir = "model/"
# the calibrated models will be saved here

# code begins here:

# load models
models = dict()
for a in alphas:
    model = BaoRegression(verbose=True, alpha=a)
    model.load(model_dir + "/" + str(a) + '/')
    models[a] = model

test_query = "SELECT COUNT(*) FROM title t WHERE t.production_year>2004;"

# generate multiple plans for the test query

# connect to the same database (should be done before the query is given)
conn = psycopg2.connect("dbname=imdb user=postgres")
conn.autocommit = True
cur = conn.cursor()
cur.execute("SET max_parallel_workers_per_gather = 0; commit;")

# using different hints to generate candidate plans
plans = []
for c in ["SET enable_seqscan = OFF", "SET enable_bitmapscan = OFF", "SET enable_indexscan = OFF", "SET enable_indexonlyscan = OFF"]:
    cur.execute(c)
for c in ["SET enable_hashjoin = OFF", "SET enable_mergejoin = OFF", "SET enable_nestloop = OFF"]:
    cur.execute(c)
# for i in range(0,len(hints)):
for i in range(0,5):
    for s in hints[i]:
        cur.execute("SET enable_" + s + " = ON")
    cur.execute("EXPLAIN (FORMAT JSON)" + test_query)
    analyze_fetched = cur.fetchall()
    a_plan = analyze_fetched[0][0][0]
    plans.append(a_plan)
    for s in hints[i]:
        cur.execute("SET enable_" + s + " = OFF")
        
# generate the execution time distribution for each candidate plan:
for alpha in alphas:
    upper_bound_times = models[alpha].predict(plans).flatten().tolist()
    print("the execution time upper bound of eah plan under prob. level", 1-alpha, ":", upper_bound_times)
