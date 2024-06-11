#!/bin/sh
#SBATCH --partition=thcp3
#SBATCH --nodes=8
export ROMIO_HINTS=romio_hints
srun -p thcp3 -N 8 -n 128 /thfs3/home/xjtu_cx/hugo/ior-main-0/bin/ior -t 4m -b 64m -s 2 -C -a MPIIO