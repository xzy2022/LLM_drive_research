#!/usr/bin/env bash
set -e
CU13=/data/xxx/conda/envs/vllm/lib/python3.12/site-packages/nvidia/cu13
cd "$CU13"
ln -sf lib lib64

cd "$CU13/lib"
ln -sf libcudart.so.13 libcudart.so
ln -sf libcublas.so.13 libcublas.so
ln -sf libcublasLt.so.13 libcublasLt.so
ln -sf libcufft.so.12 libcufft.so
ln -sf libcurand.so.10 libcurand.so
ln -sf libcusolver.so.12 libcusolver.so
ln -sf libcusparse.so.12 libcusparse.so
ln -sf libnvrtc.so.13 libnvrtc.so
ln -sf libnvJitLink.so.13 libnvJitLink.so

mkdir -p stubs
ln -sf /lib/x86_64-linux-gnu/libcuda.so stubs/libcuda.so
ln -sf /lib/x86_64-linux-gnu/libcuda.so libcuda.so

echo "Checking cu13/lib64/libcudart.so and stubs:"
ls -l "$CU13/lib64/libcudart.so"
ls -l "$CU13/lib64/stubs/libcuda.so"
