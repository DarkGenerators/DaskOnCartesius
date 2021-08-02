import os
import shlex
import subprocess

import dask.array as da

from dask.distributed import Client

from dask_jobqueue import SLURMCluster


def run_command(command):
  """ Run command """
  command_args = shlex.split(command)
  try:
    res = subprocess.run(
      command_args,
      capture_output=True,
      text=True,
      check=True,
    )
    out = res.stdout
  except subprocess.CalledProcessError as exc:
    out = exc.output, exc.stderr, exc.returncode
  return out


cluster = SLURMCluster(
    queue="short",  # "normal" or "gpu" (max 5d),
                        # "short" or "gpu_short" (max 1h)
    memory="60GB",  # memory per node
    processes=2,  # num workers per node
    cores=2,  # num threads per node
    job_mem="60GB",  # per job
    job_cpu=24,  # per job
    local_directory="$TMPDIR",
    walltime="01:00:00"
)
print(cluster.job_script())

cluster.scale(jobs=2)
client = Client(cluster)


Z = da.random.random((1000, 1000), chunks=(200, 200))
res = da.dot(Z.T, Z).mean(axis=1).max()
print(res.compute())
# 262.4432374230036

res = []
command = "srun -c 12 /home/username/DaskOnCartesius/examples/hello_world_openmp/hello_world.x"
for i in range(2):
  f = client.submit(run_command, command, pure=False)
  res.append(f)
res = client.gather(res)
print(res)
# [' Hello from thread:            3\n Hello from thread:            0\n Hello from thread:           10\n Hello from thread:            1\n Hello from thread:            9\n Hello from thread:            5\n Hello from thread:            8\n Hello from thread:            4\n Hello from thread:            6\n Hello from thread:            7\n Hello from thread:           11\n Hello from thread:            2\n', ' Hello from thread:            4\n Hello from thread:            1\n Hello from thread:            6\n Hello from thread:            8\n Hello from thread:           11\n Hello from thread:           10\n Hello from thread:            2\n Hello from thread:            0\n Hello from thread:            9\n Hello from thread:            3\n Hello from thread:            7\n Hello from thread:            5\n']
