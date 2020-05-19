#!/bin/bash
#SBATCH --job-name=pretrain-%j
#SBATCH -p titanx-long
#SBATCH -N 1
#SBATCH --gres=gpu:1
#SBATCH --output=pretrain%j.out
#SBATCH --mem=50000

module load cuda90/toolkit
modele load python3/current
module load nccl2
srun python3 run_language_modeling.py \
    --overwrite_output_dir \
    --output_dir=chkpts/ \
    --model_type roberta \
    --model_name_or_path=./chkpts/ \
    --do_train \
    --do_lower_case \
    --train_data_file=train.txt \
    --do_eval \
    --do_predict \
    --evaluate_during_training \
    --eval_data_file=test.txt \
    --mlm \
    --eval_all_checkpoints \ 
    --learning_rate =1e-8 \
    --num_train_epochs = 15 \
    --save_steps =1000 \
    --per_gpu_train_batch_size 1\
    --per_gpu_eval_batch_size 1 \
    --gradient_accumulation_steps=2
