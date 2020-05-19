#!/bin/bash
#SBATCH --job-name=diff-%j
#SBATCH -p titanx-long
#SBATCH -N 1
#SBATCH --gres=gpu:1
#SBATCH --output=diff%j.out
#SBATCH --mem=10000

module load cuda90/toolkit
module load nccl2
srun python3 /mnt/nfs/scratch1/nagarwal/CS696_Stock_fundamental_prediction/cs696_scraping/unstructured/differenceTextSentence.py
