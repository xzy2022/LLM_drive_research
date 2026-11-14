#!/usr/bin/env bash
set -Eeuo pipefail

prefix=/data/xxx/conda/envs/vllm
record=/data/xxx/setup_records/exp_1112_02_vllm_environment
conda_bin=/home/user/miniconda3/bin/conda
pip_index=${VLLM_PIP_INDEX_URL:-https://pypi.tuna.tsinghua.edu.cn/simple}
mkdir -p "$record" /data/xxx/cache/conda-pkgs /data/xxx/cache/pip
exec > >(tee -a "$record/install.log") 2>&1
trap 'rc=$?; printf "INSTALL_FAILED exit=%s time=%s\n" "$rc" "$(date -Is)"; exit "$rc"' ERR
printf 'INSTALL_STARTED %s\n' "$(date -Is)"
printf 'PREFIX=%s\nHTTP_PROXY=%s\n' "$prefix" "${http_proxy:-unset}"
curl -q -4 -fsS --connect-timeout 5 --max-time 20 https://www.cloudflare.com/cdn-cgi/trace
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv
if [[ -e "$prefix" && ! -x "$prefix/bin/python" ]]; then
    echo "Refusing to overwrite an existing incomplete directory: $prefix" >&2
    exit 1
fi

# Per-process cache/channel selection; do not modify existing Conda settings.
export CONDA_PKGS_DIRS=/data/xxx/cache/conda-pkgs
export PIP_CACHE_DIR=/data/xxx/cache/pip
export PIP_DISABLE_PIP_VERSION_CHECK=1
export PYTHONUNBUFFERED=1
export TRITON_CACHE_DIR=/data/xxx/cache/triton
if [[ ! -x "$prefix/bin/python" ]]; then
    "$conda_bin" create --prefix "$prefix" python=3.12 pip -y \
        --override-channels -c https://conda.anaconda.org/conda-forge
fi
"$prefix/bin/python" -c 'import sys; assert sys.version_info[:2] == (3, 12); print(sys.executable, sys.version)'
printf 'PIP_INDEX=%s\n' "$pip_index"
"$prefix/bin/python" -m pip install --index-url "$pip_index" \
    --only-binary=vllm,torch --retries 5 --timeout 60 --progress-bar off \
    --constraint "$record/cuda-constraints.txt" \
    --report "$record/pip-install-report.json" 'vllm==0.33.0'
"$prefix/bin/python" -m pip check
export CUDA_HOME="$prefix/lib/python3.12/site-packages/nvidia/cu13"
export PATH="$prefix/bin:$PATH"
"$conda_bin" env config vars set --prefix "$prefix" \
    "CUDA_HOME=$CUDA_HOME" "TRITON_CACHE_DIR=$TRITON_CACHE_DIR"
"$prefix/bin/python" "$record/verify.py" | tee "$record/verification.json"
"$prefix/bin/python" -m pip freeze > "$record/requirements-freeze.txt"
"$conda_bin" list --prefix "$prefix" --explicit > "$record/conda-explicit.txt"
du -sh "$prefix" /data/xxx/cache/conda-pkgs /data/xxx/cache/pip
printf 'INSTALL_COMPLETED %s\n' "$(date -Is)"
