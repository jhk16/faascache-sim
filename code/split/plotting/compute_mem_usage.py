#!/usr/bin/python3
from collections import defaultdict
import numpy as np
import multiprocessing as mp
import pickle
from collections import defaultdict
import os
from pprint import pprint
from math import floor
from datetime import datetime
import pandas as pd

import matplotlib as mpl
mpl.rcParams.update({'font.size': 14})
mpl.use('Agg')
import matplotlib.pyplot as plt
import argparse

# data_path = "/data2/alfuerst/azure/functions/trace_runs_updated"
#  memory_path = "/data2/alfuerst/azure/functions/trace_runs_rep_392/memory"
#  log_dir = "/data2/alfuerst/azure/functions/trace_runs_rep_392/logs/"
memory_path = "./trace_output/representative/memory/"
log_dir = "./trace_output/representative/logs/"

def get_info_from_file(filename):
    policy, num_funcs, mem, run, _ = filename[:-5].split("-")
    return policy, int(num_funcs), int(mem), run

def load_data(path):
    with open(path, "r+b") as f:
        return pickle.load(f)

def compute_mem_per_min(file, ret=False):
    pth = os.path.join(log_dir, file)
    policy, num_funcs, mem_cap, run = get_info_from_file(file)
    memUsageFname = os.path.join(log_dir, file)
    if policy != 'TTL':
        return

    print(file)

    try:
        df = pd.read_csv(memUsageFname, usecols = [0, 1, 2, 3, 5])
    except:
        raise
    start = {"time":0, "reason":"fix","mem_used":df.at[0, "mem_used"], "mem_size":0, "extra":"N/A"}
    end = {"time": 24 * 59 * 60 * 1000, "reason": "fix", "mem_used": df.at[len(df)-1, "mem_used"], "mem_size": 0, "extra": "N/A"}
    # print(start)
    # print(end)
    df2 = pd.DataFrame([start, end], columns=df.columns)
    df3 = pd.concat([df, df2])

    sort = df.sort_values(by=["time", "mem_used"])
    dedup = sort.drop_duplicates(subset=["time"], keep="last")
    dedup.loc[:, 'time'] = dedup['time'].apply(lambda x : datetime.fromtimestamp(x / 1000))

    dedup.set_index('time', inplace=True)
    dedup = dedup['mem_used']
    # upsample to second detail since there may be gaps
    # then downsample to minute buckets for 
    dedup = dedup.resample("S").mean().interpolate().resample("1min").interpolate()

    save_path = "{}-{}-{}-{}.npy".format(policy, num_funcs, mem_cap, run)
    save_path = os.path.join(memory_path, save_path)

    # d = dedup["mem_used"].to_numpy(copy=True)
    d = dedup.to_numpy(copy=True)
    if len(d) != 1440:
        d.resize(1440)
    # saved as numpy array in one minute buckets of average memory usage across the minute
    np.save(save_path, d)

def compute_all():
    with mp.Pool() as pool:
        files = [file for file in os.listdir(log_dir) if os.path.isfile(os.path.join(log_dir, file)) and "memusagehist" in file]
        print("computing {} files".format(len(files)))
        pool.map(compute_mem_per_min, files)

def compute_all_seq():
    files = [file for file in os.listdir(log_dir) if os.path.isfile(os.path.join(log_dir, file)) and "memusagehist" in file]
    print("computing {} files".format(len(files)))
    for f in files:
        compute_mem_per_min(f)


def compute_one():
    data = np.zeros(60*24)
    events = 0
    cnt = 0
    for file in os.listdir(log_dir):
        if "TTL-1000-4096-" in file:
            cnt += 1
            pth = os.path.join(log_dir, file)
            data += compute_mem_per_min(pth, ret=True)

    data = data / cnt
    print(cnt)
    print(data)
    print(data.mean())

if __name__ == "__main__":
    # pth = "TTL-392-16000-b-memusagehist.csv"
    # compute_mem_per_min(pth)
    # compute average memory usage per-minute of each run

    parser = argparse.ArgumentParser(description='analyze FaasCache Simulation')
    parser.add_argument("--savedir", type=str, default="/data2/alfuerst/verify-test/memory/", required=False)
    parser.add_argument("--logdir", type=str, default="/data2/alfuerst/verify-test/logs/", required=False)
    args = parser.parse_args()
    log_dir= args.logdir
    memory_path = args.savedir

    # compute_all()
    compute_all_seq()
