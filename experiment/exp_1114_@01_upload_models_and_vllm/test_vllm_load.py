import time
import torch
from vllm import LLM, SamplingParams

def main():
    model_path = "/data/xxx/models/DeepSeek-R1-Distill-Qwen-1.5B"
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Testing vLLM loading on GPU 0...")
    print(f"PyTorch version: {torch.__version__}, CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"Device name: {torch.cuda.get_device_name(0)}")

    print(f"Loading model: {model_path}")
    llm = LLM(
        model=model_path,
        tensor_parallel_size=1,
        gpu_memory_utilization=0.6,
        trust_remote_code=True
    )

    prompts = [
        "Hello, my name is",
        "The future of artificial intelligence is",
        "Please provide a one-sentence summary of autonomous driving."
    ]

    sampling_params = SamplingParams(temperature=0.7, top_p=0.9, max_tokens=50)

    print("Running generation...")
    outputs = llm.generate(prompts, sampling_params)

    for output in outputs:
        prompt = output.prompt
        generated_text = output.outputs[0].text
        print(f"\n--- PROMPT: {prompt} ---\nRESPONSE: {generated_text.strip()}\n")

    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Model loaded and generated successfully!")

if __name__ == "__main__":
    main()
