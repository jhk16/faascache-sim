#!/bin/bash
set -ex

#logdir='/data2/alfuerst/verify-test/logs'
#memstep=3000
#numfuncs=392
#savedir='/data2/alfuerst/verify-test'
# tracedir='/data2/alfuerst/azure/functions/trace_pckl/represent'
trace_dir='./trace/representative'
# trace_dir="/data2/alfuerst/azure/functions/trace_pckl/precombined"
# trace_output_dir="/data2/alfuerst/verify-test"
trace_output_dir="./trace_output/representative"
log_dir="$trace_output_dir/logs"
memory_dir="$trace_output_dir/memory"
invoke_dir="$trace_output_dir/invoke"
container_dir="$trace_output_dir/container"
analyzed_dir="$trace_output_dir/analyzed"
# plot_dir="/home/alfuerst/repos/faas-keepalive-20/code/split/figs/test/"
plot_dir="./figs/represent/"
# num_funcs=392
# num_funcs=80
num_funcs=4

mkdir -p $trace_dir
mkdir -p $trace_output_dir
mkdir -p $log_dir
mkdir -p $memory_dir
mkdir -p $analyzed_dir
mkdir -p $plot_dir

## paper used 500 simulation, but 3000 is used here for faster results
# memstep=3000
memstep=100

## Download trace
# if [[ ! -e azurefunctions-dataset2019 ]]; then
#         wget -nc "https://azurepublicdatasettraces.blob.core.windows.net/azurepublicdatasetv2/azurefunctions_dataset2019/azurefunctions-dataset2019.tar.xz"
#         tar -xvf azurefunctions-dataset2019.tar.xz
# fi

# pushd ./split/gen

## Load trace and join invocations, duration, memory
# python3 trace_split_funcs.py

## Sample functions from trace
# python3 ./split/gen/gen_representative_trace.py

# popd

## Run simulation
python3 ./split/many_run.py --tracedir $trace_dir --numfuncs $num_funcs --savedir $trace_output_dir --logdir $log_dir --memstep=$memstep

## Analyze results

# python3 ./split/plotting/compute_mem_usage.py --logdir $log_dir --savedir $memory_dir
# python3 ./split/plotting/compute_invocation.py --logdir $log_dir --savedir $invoke_dir
# python3 ./split/plotting/compute_pure_cache.py --logdir $log_dir --savedir $memory_dir --numfuncs $num_funcs

# python3 ./split/plotting/compute_container_total.py --logdir $log_dir --savedir $container_dir
# python3 ./split/plotting/compute_container_running.py --logdir $log_dir --savedir $container_dir
# python3 ./split/plotting/compute_container_concurrency.py --logdir $log_dir --savedir $container_dir

# python3 ./split/plotting/compute_policy_results.py --pckldir $trace_output_dir --savedir $analyzed_dir

## Plot graphs

# python3 ./split/plotting/plot_many.py
# python3 ./split/plotting/plot_dropped.py

# python3 ./split/plotting/plot_run_across_mem.py --analyzeddir $analyzed_dir --plotdir $plot_dir --numfuncs $num_funcs
# python3 ./split/plotting/plot_cold_across_mem.py --analyzeddir $analyzed_dir --plotdir $plot_dir --numfuncs $num_funcs
# python3 ./split/plotting/plot_cold_percent.py --analyzeddir $analyzed_dir --plotdir $plot_dir --numfuncs $num_funcs

# python3 ./split/plotting/plot_invocation.py --invokedir $invoke_dir --plotdir $plot_dir --numfuncs $num_funcs

# Memory usage
# python3 ./split/plotting/plot_mem_usage.py --memorydir $memory_dir --plotdir $plot_dir --numfuncs $num_funcs
# python3 ./split/plotting/plot_container_usage.py --containerdir $container_dir --plotdir $plot_dir --numfuncs $num_funcs
