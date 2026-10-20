---
name: pytorch-experiments
description: "Run reproducible PyTorch training and evaluation: seeding, deterministic data splits and leakage checks, checkpoints that can resume, GPU memory and throughput benchmarking, and ONNX export with output verification. Use when training or evaluating a PyTorch model, benchmarking a GPU, or preparing a model for deployment."
---

# PyTorch Experiments

Treat each training run as an experiment you may need to repeat, audit, or resume. Record everything that could change the result, make the data split before any other step, and verify exported models against the original rather than trusting the export.

## Step 1: Make the run reproducible

```python
import random, numpy as np, torch

def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
```

- Seed each `DataLoader` worker with `worker_init_fn` and a `torch.Generator` for shuffling. Otherwise workers reuse the same random streams.
- Determinism costs speed. Keep `cudnn.benchmark = False` for reproducible comparisons and turn it on only for throughput runs.
- Write a run record next to the checkpoint: git commit, seed, config, library versions (`torch.__version__`, CUDA version, GPU name), and dataset hash.

## Step 2: Split data before anything else

- Split by the unit that must not leak: patient, session, camera, episode, or sequence. A random frame-level split of correlated frames inflates validation scores.
- Fit normalisation statistics on the training split only.
- Apply augmentation to training data only, after the split.
- Check for leakage explicitly: count identical or near-identical samples across splits and report the number.

## Step 3: Training loop essentials

- Save a checkpoint containing model `state_dict`, optimiser and scheduler state, the epoch, the best metric, and the RNG state. A checkpoint without optimiser state cannot resume faithfully.
- Use `torch.autocast` for mixed precision on CUDA. Confirm loss stays finite, and log any loss-scaling skips.
- Evaluate with `model.eval()` and `torch.no_grad()` (or `torch.inference_mode()`). Forgetting `eval()` silently changes dropout and batch-norm behaviour.
- Report the validation metric with the checkpoint it came from, not the last epoch's value.

## Step 4: GPU benchmarking and memory

Warm up before timing, synchronise before reading the clock, and report medians over repeated runs:

```python
import time, torch

def benchmark(fn, *, warmup=10, iters=50):
    for _ in range(warmup):
        fn()
    torch.cuda.synchronize()
    times = []
    for _ in range(iters):
        start = time.perf_counter()
        fn()
        torch.cuda.synchronize()
        times.append(time.perf_counter() - start)
    times.sort()
    return times[len(times) // 2]   # median seconds per call

torch.cuda.reset_peak_memory_stats()
# ... run the workload ...
print(torch.cuda.max_memory_allocated() / 2**20, "MiB peak allocated")
```

- `nvidia-smi` shows reserved memory, which includes PyTorch's cache. `max_memory_allocated()` shows what tensors actually used.
- If memory is tight, try in this order: smaller batch, gradient accumulation, mixed precision, activation checkpointing (`torch.utils.checkpoint`), then a smaller model.
- Compare throughput at the same batch size and precision only.

## Step 5: Evaluation and reporting

- Report per-class or per-slice metrics, not only the aggregate. Class imbalance can hide a collapsed class.
- Keep a fixed held-out test set that is touched once, after model selection.
- Store predictions and metrics as files alongside the run record so a result can be re-derived later.

## Step 6: ONNX export and verification

```python
import torch

model.eval()
dummy = torch.randn(1, 3, 224, 224, device="cpu")   # use the real input shape
torch.onnx.export(
    model.cpu(), dummy, "model.onnx",
    input_names=["input"], output_names=["output"],
    dynamic_axes={"input": {0: "batch"}, "output": {0: "batch"}},
)
```

Verify the export before using it:

```python
import numpy as np, onnxruntime as ort

session = ort.InferenceSession("model.onnx", providers=["CPUExecutionProvider"])
ref = model(dummy).detach().numpy()
out = session.run(None, {"input": dummy.numpy()})[0]
np.testing.assert_allclose(ref, out, rtol=1e-3, atol=1e-4)
```

- Compare on several real inputs, not only the dummy tensor.
- Check the exporter version and opset in the run record. Export APIs change between PyTorch releases.
- For inference speed, benchmark the ONNX model with the same harness as the PyTorch model, on the target hardware.

## Reporting

Report the seed, split method and leakage check, the checkpoint used, the metric with its confidence or variance across seeds when available, the hardware, and any step you could not run (for example, the ONNX check on the target device).
