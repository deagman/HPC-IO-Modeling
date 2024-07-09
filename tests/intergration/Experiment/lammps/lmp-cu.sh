#!/bin/bash
#SBATCH -p thcp3
#SBATCH -N 32
#SBATCH -n 512
#export ROMIO_HINTS=romio_hints
mkdir result
srun -p thcp3 -N 32 -n 521 /thfs3/home/xjtu_cx/hugo/lammps-29Sep2021/install/bin/lmp -in cu.lammps
rm -rf result