#!/bin/bash
#SBATCH --job-name=roberta_race-%j
#SBATCH -p m40-long
#SBATCH -N 1
#SBATCH --gres=gpu:2
#SBATCH --output=models/logs/%j.out
#SBATCH --mem=50000
module load cuda90/toolkit
module load /home/nagarwal/anaconda3/bin
srun python3 -m torch.distributed.launch \
--nproc_per_node=1 ./cs696_scraping/unstructured/main.py