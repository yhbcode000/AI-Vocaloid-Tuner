import sys, os
sys.path.append(os.getcwd())

from vocaloidDao import vocaloidVSQXResolver
import json

dataPath = os.path.join(os.getcwd(), 'VocaloidVSQXCollection')

with open(os.path.join(dataPath,"source.json"), 'r') as f:
    source = json.load(f)

fileList = [source["source-"+str(sourceIndex+1)]["file"] for sourceIndex in range(len(source))]

resolverList = [vocaloidVSQXResolver(os.path.join(dataPath, fileName)) for fileName in fileList]


import datetime
import multiprocessing as mp

def func(dataPath, resolver):
    return resolver.saveFormatedVocaloidData(resolver.getFormatedVocaloidDataInDict(), dataPath)

# # initialise the pool
num_cores = int(mp.cpu_count())
print("local computer has: " + str(num_cores) + " cores\n")
pool = mp.Pool(num_cores)

# # prepare processes not starting any process
processes = [pool.apply_async(func, args=(dataPath, resolver,)) for resolver in resolverList if not(
    os.path.exists(os.path.join(dataPath, resolver.resolverIdentifier[:-5]+"DataDict.csv")))]

start_t = datetime.datetime.now()
results = [p.get() for p in processes]
end_t = datetime.datetime.now()

elapsed_sec = (end_t - start_t).total_seconds()
print("Parallal computing takes " + "{:.2f}".format(elapsed_sec) + " seconds to finish.\n")
