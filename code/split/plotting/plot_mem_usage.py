#!/usr/bin/python3
from collections import defaultdict
import numpy as np
import multiprocessing as mp
import pickle
from collections import defaultdict
import os
from pprint import pprint
from math import floor
import sys

import matplotlib as mpl
mpl.rcParams.update({'font.size': 14})
mpl.use('Agg')
import matplotlib.pyplot as plt
import argparse

memory_path = "/data2/alfuerst/azure/functions/trace_runs_rep_392/memory"

def get_info_from_file(filename):
    policy, num_funcs, mem, run, stat = filename[:-4].split("-")
    print(stat)
    return policy, int(num_funcs), int(mem), run, stat

def plot_run(data_dict, memory, num_funcs):
    colors = ["tab:blue", "tab:green", "tab:orange", "tab:purple", "tab:brown", "tab:pink", "tab:gray"]
    # Plot total memory
    stat = 'total'
    fig, ax = plt.subplots()
    plt.tight_layout()
    fig.set_size_inches(5,3)
    ax.set_ylabel("Memory usage (MB)")
    ax.set_xlabel("Time (min)")
    # print(data_dict)
    for policy in sorted(data_dict.keys()):
        avg_mem = np.zeros(60*24, dtype=np.float64)
        for arr in data_dict[policy]['total']:
            avg_mem += arr

        avg_mem = avg_mem / len(data_dict[policy]['total'])
        ax.plot([i for i in range(60*24)], avg_mem, label=policy + '-' + 'total', color=colors[0])
    ax.axhline(y=memory, color="red")
    fig.legend()
    # save_path = os.path.join(plot_dir, "mem-usage-{}-{}.pdf".format(memory, num_funcs))
    save_path = os.path.join(plot_dir, "mem-usage-{}-{}-{}.png".format(memory, num_funcs, stat))
    plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(save_path)

    # Plot total + running memory
    fig, ax = plt.subplots()
    plt.tight_layout()
    fig.set_size_inches(5,3)
    ax.set_ylabel("Memory usage (MB)")
    ax.set_xlabel("Time (min)")
    # print(data_dict)
    for policy in sorted(data_dict.keys()):
        for i, stat in enumerate(data_dict[policy]):
            if stat == 'pure_cache':
                continue
            avg_mem = np.zeros(60*24, dtype=np.float64)
            for arr in data_dict[policy][stat]:
                avg_mem += arr

            avg_mem = avg_mem / len(data_dict[policy][stat])
            ax.plot([i for i in range(60*24)], avg_mem, label=policy + '-' + stat, color=colors[i])
    ax.axhline(y=memory, color="red")
    fig.legend()
    # save_path = os.path.join(plot_dir, "mem-usage-{}-{}.pdf".format(memory, num_funcs))
    save_path = os.path.join(plot_dir, "mem-usage-{}-{}-{}.png".format(memory, num_funcs, 'total_running'))
    plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(save_path)

    # Plot total + pure cache
    fig, ax = plt.subplots()
    plt.tight_layout()
    fig.set_size_inches(5,3)
    ax.set_ylabel("Memory usage (MB)")
    ax.set_xlabel("Time (min)")
    # print(data_dict)
    for policy in sorted(data_dict.keys()):
        for i, stat in enumerate(data_dict[policy]):
            if stat == 'running':
                continue
            avg_mem = np.zeros(60*24, dtype=np.float64)
            for arr in data_dict[policy][stat]:
                avg_mem += arr

            avg_mem = avg_mem / len(data_dict[policy][stat])
            ax.plot([i for i in range(60*24)], avg_mem, label=policy + '-' + stat, color=colors[i])
    ax.axhline(y=memory, color="red")
    fig.legend()
    # save_path = os.path.join(plot_dir, "mem-usage-{}-{}.pdf".format(memory, num_funcs))
    save_path = os.path.join(plot_dir, "mem-usage-{}-{}-{}.png".format(memory, num_funcs, 'total_purecache'))
    plt.savefig(save_path, bbox_inches="tight")
    plt.close(fig)
    print(save_path)


def plot_all(args):
    data = dict()
    funcs = args.numfuncs
    filt = "-{}-".format(funcs)
    for file in os.listdir(memory_path):
        if filt in file and "b" in file:
            print(file)
            policy, num_funcs, mem, run, stat = get_info_from_file(file)
            # saved as numpy array in one minute buckets of average memory usage across the minute
            array = np.load(os.path.join(memory_path, file))
            if mem not in data:
                data[mem] = dict()

            if num_funcs not in data[mem]:
                data[mem][num_funcs] = dict()

            if policy not in data[mem][num_funcs]:
                data[mem][num_funcs][policy] = dict()

            if stat not in data[mem][num_funcs][policy]:
                data[mem][num_funcs][policy][stat] = list()

            data[mem][num_funcs][policy][stat].append(array)
    # print(data)

    for mem_alloc in data.keys():
        for num_funcs in data[mem_alloc].keys():
            plot_run(data[mem_alloc][num_funcs], mem_alloc, num_funcs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='plot FaasCache Simulation')
    parser.add_argument("--memorydir", type=str, default="/data2/alfuerst/verify-test/analyzed", required=False)
    parser.add_argument("--plotdir", type=str, default="../figs/increase_with_mem/", required=False)
    parser.add_argument("--numfuncs", type=int, default=392, required=False)
    args = parser.parse_args()
    memory_path = args.memorydir
    plot_dir = args.plotdir

    plot_all(args)
