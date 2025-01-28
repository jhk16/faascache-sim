import numpy as np
import pandas as pd
import os
import sys
import json
from time import time

from wsk_interact import *

import pickle

class LambdaData:
    def __init__ (self, kind, mem_size, run_time, warm_time):
        self.kind = kind 
        self.mem_size = mem_size
        self.run_time = run_time 
        self.warm_time = warm_time
        
    def __eq__(self, other):
        if isinstance(other, LambdaData):
            return self.kind == other.kind 
        
    def __repr__(self):
        return str((self.kind, self.mem_size))

# set_properties()
pth = "./traces/freq_litmus_sub.pckl"
with open(pth, "r+b") as f:
    trace = pickle.load(f)
    # print(trace)
for tup in trace:
    hash_app, invoc_time_ms, mem, warm, cold = tup
    print(tup)
sys.exit()

# pth = "/data2/alfuerst/azure/functions/trace_pckl/precombined/{}-{}.pckl".format(num_functions, char)
pth = "/home/jonghyeon/research/faascache-sim/code/trace/representative/392-c.pckl"
with open(pth, "r+b") as f:
    lambdas, trace = pickle.load(f)
    print(trace)
    data = pickle.load(f)
sys.exit()

for action, metadata in lambdas.items():
    hash_app, memory, _, _ = metadata
    # add_action(action,  "./lookbusy/__main__.py", container="python:lookbusy", memory=memory)
    container = "tome01/lookbusy"
    path = "./lookbusy/__main__.py"
    name = hash_app

    # add_action(hash_app, "./lookbusy/__main__.py", container="python:lookbusy", memory=mem)
    # print("added {}".format(hash_app))
    args = ["wsk", "-i", "action", "update", name, "--memory", '300', "--docker", container, path]
    print(args)
    wsk = subprocess.run(args=args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

start = time()
# LambdaData, time
for d, invoc_time_ms in trace:
    # print(d.kind, invoc_time_ms)
    # hash_app, mem = lambdas[0], lambdas[1]
    hash_app = d.kind
    cold = d.run_time
    warm = d.warm_time
    mem = d.mem_size

    t = time()
    # hash_app, invoc_time_ms, mem, warm, cold = tup
    name = hash_app

    invoc_time = invoc_time_ms / 1000 # convert ms to float s
    while t - start < invoc_time:
        t = time()
    # invoke_action_async(hash_app, {"cold_run":cold, "warm_run":warm, "mem_mb":mem})
    popen_args = ["wsk", "-i", "action", "invoke", name]
    act_args = {"cold_run":cold, "warm_run":warm, "mem_mb":mem}
    for key, value in act_args.items():
        popen_args += ["--param", str(key), str(value)]
    wsk = subprocess.Popen(args=popen_args)

