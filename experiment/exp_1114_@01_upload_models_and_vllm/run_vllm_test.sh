#!/usr/bin/env bash
set -e
source /home/user/miniconda3/etc/profile.d/conda.sh
conda activate /data/xxx/conda/envs/vllm
export CUDA_VISIBLE_DEVICES=0
python /data/xxx/test_vllm_load.py
