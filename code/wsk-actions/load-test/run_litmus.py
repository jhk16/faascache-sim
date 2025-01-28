import numpy as np
import os
from time import time
import pickle

# from wsk_interact import add_action, invoke_action_async, set_properties
import subprocess

# set_properties()

# Traces are list of tuples
# of (action_name, invocation_time, memory_usage, cold_time, warm_time)

freq = "./traces/freq_litmus.pckl"
iat = "./traces/iat_litmus.pckl"
lru = "./traces/lru_litmus.pckl"
size = "./traces/size_litmus.pckl"

load = lru

with open(load, "r+b") as f:
    trace = pickle.load(f)

# print(trace)
names = set([i[0] for i in trace])
# print(names)

dedup = []
for item in names:
    for t in trace:
        if t[0] == item:
            dedup.append(t)
            break

print(dedup)
for tup in dedup:
    hash_app, invoc_time_ms, mem, warm, cold = tup
    container = "tome01/lookbusy"
    path = "./lookbusy/__main__.py"
    name = hash_app

    # add_action(hash_app, "./lookbusy/__main__.py", container="python:lookbusy", memory=mem)
    # print("added {}".format(hash_app))
    args = ["wsk", "-i", "action", "update", name, "--memory", str(mem), "--docker", container, path]
    print(args)
    wsk = subprocess.run(args=args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if wsk.returncode != 0:
        print(wsk.stderr)
        wsk.check_returncode()
    wsk.check_returncode()

start = time()
for tup in trace:
    print(tup)
    t = time()
    hash_app, invoc_time_ms, mem, warm, cold = tup
    name = hash_app

    invoc_time = invoc_time_ms / 1000 # convert ms to float s
    while t - start < invoc_time:
        t = time()

    # print(hash_app, {"cold_run":cold, "warm_run":warm, "mem_mb":mem})
    # popen_args = ["wsk", "-i", "action", "invoke", "--result", name]
    popen_args = ["wsk", "-i", "action", "invoke", name]
    act_args = {"cold_run":cold, "warm_run":warm, "mem_mb":mem}
    for key, value in act_args.items():
        popen_args += ["--param", str(key), str(value)]
    wsk = subprocess.Popen(args=popen_args)

# #     invoke_action_async(hash_app, {"cold_run":cold, "warm_run":warm, "mem_mb":mem})
