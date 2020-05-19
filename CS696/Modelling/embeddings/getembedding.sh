#!/bin/bash
#SBATCH --job-name=embedding-%j
#SBATCH -p titanx-long
#SBATCH -N 1
#SBATCH --gres=gpu:1
#SBATCH --output=em%j.out
#SBATCH --mem=15000

module load cuda90/toolkit
module load nccl2
srun python3 -m torch.distributed.launch --nproc_per_node=1 /mnt/nfs/scratch1/nagarwal/CS696_Stock_fundamental_prediction/cs696_scraping/unstructured/modelling/main.py
