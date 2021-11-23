import os
import subprocess

import dask.array as da

from dask.distributed import Client

from dask_jobqueue import SLURMCluster


def run_command(command):
  """ Run command """
  try:
    res = subprocess.run(
      command,
      capture_output=True,
      text=True,
      check=True,
      shell=True,
    )
    out = res.stdout
  except subprocess.CalledProcessError as exc:
    out = exc.output, exc.stderr, exc.returncode
  return out


cluster = SLURMCluster(
    queue="thin",
    memory="60GiB",  # max memory per job
    processes=2,  # num workers per job
    cores=2,  # num threads per job
    job_cpu=24,  # num cores per SLURM job (-c/--cpus-per-task)
    local_directory="$TMPDIR",
    walltime="01:00:00"
)
print(cluster.job_script())

cluster.scale(jobs=2)
client = Client(cluster)


Z = da.random.random((1000, 1000), chunks=(200, 200))
res = da.dot(Z.T, Z).mean(axis=1).max()
print(res.compute())

res = []
command = ("module load 2021 &&"
           "module load iompi/2021a &&"
           "srun -c 16 /home/username/DaskOnSnellius/examples/hello_world/hello_world_openmp/hello_world.x")

for i in range(4):
  f = client.submit(run_command, command, pure=False)
  res.append(f)
res = client.gather(res)
print(res)
