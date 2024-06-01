#!/bin/sh

# 设置输出文件路径
#SBATCH --output=/path/to/slurm-%j.out

slurm_nodelist=$SLURM_NODELIST
echo "Program is running on nodes: $slurm_nodelist"

# Direct I/O settings
export IOR_HINT__MPI__direct_read=$direct_read
export IOR_HINT__MPI__direct_write=$direct_write

# Data Sieving settings
# export IOR_HINT__MPI__ind_rd_buffer_size=$ind_rd_buffer_size
# export IOR_HINT__MPI__ind_wr_buffer_size=$ind_wr_buffer_size
# export IOR_HINT__MPI__romio_ds_read=$romio_ds_read
# export IOR_HINT__MPI__romio_ds_write=$romio_ds_write

# Collective I/O settings
#export IOR_HINT__MPI__cb_config_list=*:1
#export IOR_HINT__MPI__cb_buffer_size=16777216
#export IOR_HINT__MPI__romio_cb_read=enable
#export IOR_HINT__MPI__romio_cb_write=enable

# Striping settings
export IOR_HINT__MPI__striping_unit=$striping_unit
export IOR_HINT__MPI__striping_factor=$striping_factor

# Independent IO + shared file + 写 + 读（reorder）
srun -p partition -N 1 -n 16 ior -t $transfersize -b $blocksize -s $segment -C -a MPIIO --mpiio.showHints