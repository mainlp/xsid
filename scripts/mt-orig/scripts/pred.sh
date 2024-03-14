#!/bin/bash

#SBATCH --job-name=projection
#SBATCH --output=projection.out
#SBATCH --cpus-per-task=4
#SBATCH --time=10:00:00
#SBATCH --gres=gpu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --partition=red


./predict.sh da $CUDA_VISIBLE_DEVICES
./predict.sh it $CUDA_VISIBLE_DEVICES
./predict.sh sr $CUDA_VISIBLE_DEVICES
#./predict.sh tr $CUDA_VISIBLE_DEVICES
