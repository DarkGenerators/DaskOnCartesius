# Run a command-line program across the Dask cluster

Compile the executable:
```shell
cd hello_world_openmp
bash compile.bsh
```

Modify the path to the executable in `test_cluster.py`, then submit the job script `test_cluster.bsh`:
```shell
sbatch test_cluster.bsh
```

Follow the instructions in the stdout of the batch job script (e.g. `slurm-<JOBID>.out`) to connect to the Dask dashboard. 
