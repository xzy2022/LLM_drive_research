import importlib
import importlib.metadata
import json
import platform
import sys

import torch
import torch.nn.functional as functional
import vllm
import triton
import triton.language as tl


@triton.jit
def add_one_kernel(source, destination, size: tl.constexpr, block: tl.constexpr):
    offsets = tl.program_id(0) * block + tl.arange(0, block)
    values = tl.load(source + offsets, offsets < size, other=0)
    tl.store(destination + offsets, values + 1, offsets < size)

assert sys.version_info[:2] == (3, 12), sys.version
assert importlib.metadata.version("vllm") == "0.33.0", vllm.__version__
assert torch.cuda.is_available(), "CUDA unavailable"
assert torch.cuda.device_count() == 8, torch.cuda.device_count()
compiler_packages = {
    name: importlib.metadata.version(name)
    for name in ("nvidia-cuda-nvcc", "nvidia-cuda-nvrtc", "nvidia-nvvm", "nvidia-nvjitlink", "cuda-bindings")
}
assert all(version.startswith("13.0.") for version in compiler_packages.values()), compiler_packages
gpus = []
for index in range(torch.cuda.device_count()):
    properties = torch.cuda.get_device_properties(index)
    gpus.append(
        {
            "index": index,
            "name": properties.name,
            "compute_capability": list(torch.cuda.get_device_capability(index)),
            "total_memory_bytes": properties.total_memory,
        }
    )

# Small GPU-0 checks only: no model weights, server, or multi-GPU benchmark.
with torch.inference_mode():
    matrix = torch.arange(16, device="cuda:0", dtype=torch.float32).reshape(4, 4)
    actual = matrix @ matrix.T
    reference = matrix.cpu() @ matrix.cpu().T
    torch.testing.assert_close(actual.cpu(), reference)

    # Current vLLM loads _C_stable_libtorch via its platform loader.
    from vllm.platforms import current_platform

    current_platform.import_kernels()
    inputs = torch.linspace(-2, 2, 256, device="cuda:0", dtype=torch.float16).reshape(2, 128)
    output = torch.empty((2, 64), device="cuda:0", dtype=torch.float16)
    torch.ops._C.silu_and_mul(output, inputs)
    expected = functional.silu(inputs[:, :64]) * inputs[:, 64:]
    torch.testing.assert_close(output, expected, atol=0.002, rtol=0.002)
    torch.cuda.synchronize()

    jit_input = torch.arange(256, device="cuda:0", dtype=torch.float32)
    jit_output = torch.empty_like(jit_input)
    add_one_kernel[(1,)](jit_input, jit_output, 256, 256)
    torch.cuda.synchronize()
    torch.testing.assert_close(jit_output, jit_input + 1)

print(
    json.dumps(
        {
            "python": platform.python_version(),
            "executable": sys.executable,
            "vllm": vllm.__version__,
            "torch": torch.__version__,
            "torch_cuda_runtime": torch.version.cuda,
            "cuda_available": torch.cuda.is_available(),
            "gpus": gpus,
            "gpu_matrix_check": "passed",
            "vllm_cuda_extension_import": "passed",
            "vllm_silu_and_mul_check": "passed",
            "triton_jit_check": "passed",
            "cuda_compiler_packages": compiler_packages,
            "model_inference_tested": False,
        },
        indent=2,
    )
)
