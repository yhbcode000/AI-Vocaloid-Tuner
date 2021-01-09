import os

import pandas as pd

import datetime

import multiprocessing as mp


def __func(resolver):
    return resolver.saveFormatedVocaloidData()


def parallelResolve(resolverList):
    # # initialise the pool
    num_cores = int(mp.cpu_count())
    print("local computer has: " + str(num_cores) + " cores\n")
    pool = mp.Pool(num_cores)

    # # prepare processes not starting any process
    processes = [pool.apply_async(__func, args=(resolver,)) for resolver in resolverList if not(
        os.path.exists(os.path.join(resolver.folderPath, resolver.resolverIdentifier[:-5]+"DataDict.csv")))]

    start_t = datetime.datetime.now()
    results = [p.get() for p in processes]
    end_t = datetime.datetime.now()

    elapsed_sec = (end_t - start_t).total_seconds()
    print("Parallal computing takes " +
          "{:.2f}".format(elapsed_sec) + " seconds to finish.\n")
