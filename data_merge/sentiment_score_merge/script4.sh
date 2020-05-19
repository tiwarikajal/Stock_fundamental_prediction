#!/bin/bash
#SBATCH --job-name=embedding-%j
#SBATCH -p 2080ti-short
#SBATCH -N 1
#SBATCH --gres=gpu:1
#SBATCH --output=em%j.out
#SBATCH --mem=15000

module load cuda100/10.0.130
#module load torch7/7.0
#module load python3/3.8.2-2004
#module load nccl2
srun python3 -m torch.distributed.launch --nproc_per_node=1 Final_merge4.py 
