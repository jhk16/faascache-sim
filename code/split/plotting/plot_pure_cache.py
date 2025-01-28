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
from numpy.lib.function_base import kaiser
import pandas as pd

import matplotlib as mpl
mpl.rcParams.update({'font.size': 14})
mpl.use('Agg')
import matplotlib.pyplot as plt
import argparse

memory_path = "./trace_output/representative/memory/"
log_dir = "./trace_output/representative/logs/"


def get_info_from_file(filename):
    policy, num_funcs, mem, run, _ = filename[:-5].split("-")
    return policy.split("/")[-1], int(num_funcs), int(mem), run

def compute_mem_per_min(file):
    policy, num_funcs, mem_cap, run = get_info_from_file(file)
    try:
        # cols => time, used_mem, running_mem, pure_cache
        df = pd.read_csv(file)
        print(df)
    except:
        print(file)
        raise

    sort = df.sort_values(by=["time"])
    dedup = sort.drop_duplicates(subset=["time"], keep="last")
    dedup.index = (dedup["time"] / 1000).apply(datetime.fromtimestamp)
    # upsample to second detail since there may be gaps
    # then downsample to minute buckets for
    dedup = dedup.resample("S").mean().interpolate().resample("1Min").interpolate()

    save_path = "{}-{}-{}-pure_cache-{}.npy".format(policy, num_funcs, mem_cap, run)
    save_path = os.path.join(memory_path, save_path)

    d = dedup['pure_cache'].to_numpy(copy=True)
    if len(d) != 1440:
        d.resize(1440)
    np.save(save_path, d)

    # print(dedup["used_mem"].mean())
    # print(dedup["pure_cache"].mean())
    # print(dedup["pure_cache"].mean() / dedup["used_mem"].mean())
    return mem_cap, dedup["pure_cache"].mean() / dedup["used_mem"].mean()


def compute_all():
    # data = {"GD": []}  # , "TTL":[], "HIST":[]
    data = {"TTL": []}  # , "TTL":[], "HIST":[]
    for file in os.listdir(log_dir):
        file = os.path.join(log_dir, file)
        # print(file)
        policy, num_funcs, mem_cap, run = get_info_from_file(file)
        # if os.path.isfile(file) and "b-purecachehist" in file and mem_cap < 6000:
        if os.path.isfile(file) and "b-purecachehist" in file:
            # if "GD-200" in file:
            #     mem_cap, pure = compute_mem_per_min(file)
            #     data["GD"].append((mem_cap, pure))
            # elif "HIST-200" in file:
            #     mem_cap, pure = compute_mem_per_min(file)
            #     data["HIST"].append((mem_cap, pure))
            print(file)
            if "TTL" in file:
                mem_cap, pure = compute_mem_per_min(file)
                data["TTL"].append((mem_cap, pure))
                print(data)
            else:
                pass

    fig, ax = plt.subplots()
    plt.tight_layout()
    fig.set_size_inches(5,3)
    ax.set_ylabel("Pure Cache %")
    ax.set_xlabel("Memory (MB)")
    ax.set_title("{}-b trace".format(num_funcs))
    for k, v in data.items():
        print(k,v)
        v = sorted(v, key= lambda x: x[0])
        ax.bar([x for x,y in v], [y*100 for x,y in v], label=k)
    # ax.plot([x for x,y in data["TTL"]], [y for x,y in data["TTL"]], label="TTL")
    # ax.plot([x for x, y in data["HIST"]], [y for x, y in data["HIST"]], label="HIST")

    fig.legend()
    # save_path = "../figs/represent/pure-cache-{}-b.png".format(392)
    save_path = os.path.join(plot_dir, "pure-cache-{}-b.png".format(mem_cap, num_funcs))
    plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)

def compute_one():
    for file in os.listdir(log_dir):
        if file == "GD-200-200-a-purecachehist.csv":
            pth = os.path.join(log_dir, file)
            compute_mem_per_min(pth)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='plot FaasCache Simulation')
    parser.add_argument("--logdir", type=str, default="/data2/alfuerst/verify-test/analyzed", required=False)
    parser.add_argument("--plotdir", type=str, default="../figs/increase_with_mem/", required=False)
    parser.add_argument("--numfuncs", type=int, default=392, required=False)
    args = parser.parse_args()
    log_dir = args.logdir
    memory_path = args.savedir
    plot_dir = args.plotdir

    compute_all()
