#!/bin/sh
#SBATCH -p thcp3
export ROMIO_HINTS=my_romio-hints_generated
srun -p thcp3  -N 1 -n 16 lmp_mpi -in in.box