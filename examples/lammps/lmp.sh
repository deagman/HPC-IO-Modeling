#!/bin/sh
#SBATCH -p thcp3
export ROMIO_HINTS=romio_hints
srun -p thcp3  -N 1 -n 16 lmp_mpi -in in.box