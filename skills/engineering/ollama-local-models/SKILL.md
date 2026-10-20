---
name: ollama-local-models
description: "Discover, size, run, and compare local Ollama models; check whether they fit the machine's RAM and VRAM; benchmark latency and memory; and decide when a local model should replace a cloud call. Use when choosing or evaluating a local LLM, integrating Ollama with a coding workflow, or deciding whether a model download is worth the disk space."
---

# Ollama Local Models

Check the machine before you pull anything. Model files are large, and a model that does not fit in VRAM runs partly on the CPU and can be an order of magnitude slower. Do not download a model without the user's approval; report the expected size first.

## Step 1: Inventory what is already here

```bash
ollama --version
ollama list                 # installed models and their on-disk size
ollama ps                   # models currently loaded, and the CPU/GPU split
curl -s http://127.0.0.1:11434/api/version
```

- If `curl` fails, the server is not running. Start it with `ollama serve` in its own terminal, or rely on the desktop service. Do not edit shell or service configuration to do this.
- Check hardware:
  ```bash
  free -h                                              # system RAM
  nvidia-smi --query-gpu=name,memory.total --format=csv   # VRAM, if NVIDIA
  ```

## Step 2: Estimate fit before downloading

Rough rule for 4-bit quantised models (for example `Q4_K_M`): weights take about 0.6 GB per billion parameters, plus 1 to 2 GB for the KV cache at moderate context.

| Model size (params) | Approx. weights at Q4 | Fits fully in 6 GB VRAM? |
| --- | --- | --- |
| 1–3 B | 0.6–2 GB | yes |
| 4–5 B | 2.5–3.5 GB | yes, with a moderate context |
| 7–8 B | 4.5–5 GB | borderline; long contexts spill to CPU |
| 13 B+ | 8 GB+ | no; partial CPU offload |

Use `ollama show <model>` to read the parameter count and quantisation of a model you already have, and the registry page for a model you do not. Report the estimated download size and whether it fits, then ask before pulling.

## Step 3: Run and inspect

```bash
ollama run <model> "Explain what this function does: ..."   # one-shot prompt
ollama ps                                                    # check the GPU/CPU split while it runs
```

A split such as `30%/70% CPU/GPU` means the model is too large for VRAM. Expect much lower token throughput, and prefer a smaller model or a shorter context for interactive work.

## Step 4: Call the local API

Ollama exposes a local HTTP API. Use non-streaming requests for scripted evaluation:

```bash
curl -s http://127.0.0.1:11434/api/generate -d '{
  "model": "<model>",
  "prompt": "Write a Python function that parses ISO-8601 dates.",
  "stream": false,
  "options": { "temperature": 0, "num_ctx": 4096 }
}'
```

The response contains `total_duration`, `load_duration`, `prompt_eval_count`, and `eval_count`, `eval_duration` (nanoseconds). Tokens per second is `eval_count / (eval_duration / 1e9)`.

## Step 5: Compare models fairly

Use the same prompts, the same `temperature: 0`, the same context size, and a warm model for each run. Discard the first request, which includes model load time.

Measure and record for each model:

- Latency to first token and total time for a fixed prompt set.
- Tokens per second from `eval_count` and `eval_duration`.
- Memory: `ollama ps` while loaded, and `ollama list` for disk size.
- Output quality against a small set of tasks with known correct answers. Check the answers yourself; a model judging its own output is not a valid check.

## Step 6: Decide when local is the right choice

Use a local model when:

- The data should not leave the machine (private code, credentials-adjacent logs, unpublished designs).
- The task is small and repetitive: classification, summarisation of a file, drafting commit messages, extracting fields.
- Latency matters more than peak quality, and the model is loaded once and reused.

Keep a cloud model when the task needs long context, broad knowledge, or careful multi-step reasoning, and the local model fails the quality check above.

## Step 7: Integrating with coding workflows

- Point tools that accept an OpenAI-compatible base URL at `http://127.0.0.1:11434/v1`. Check the tool's documentation for the exact setting; do not assume it.
- Keep model names in the tool's configuration, not hard-coded in scripts, so you can swap models after benchmarking.

## Reporting

Report the installed models, the hardware, the estimated size and fit of any candidate, the benchmark numbers with their conditions, and the decision with its reason. State that no model was downloaded if none was.
