---
name: edge-inference
description: "Optimize and deploy deep learning models for edge devices and robotics using ONNX Runtime, TensorRT, INT8 quantization, and hardware acceleration."
---

# Edge Inference Optimization Protocol

Use this skill when optimizing neural networks for edge compute devices (NVIDIA Jetson, Raspberry Pi, embedded Linux) and real-time robotics controllers.

## Optimization Strategy

### 1. Model Export & Representation
- Export PyTorch models to **ONNX** with fixed or explicitly bounded dynamic axes:
  ```python
  torch.onnx.export(
      model, dummy_input, "model.onnx",
      input_names=["input"], output_names=["output"],
      opset_version=17, dynamic_axes={"input": {0: "batch_size"}}
  )
  ```
- Verify operator compatibility: ensure all operations are supported in ONNX/TensorRT without falling back to CPU execution.

### 2. Quantization (FP16 / INT8)
- **FP16 Half Precision**: Double throughput on modern GPU tensor cores with negligible accuracy drop.
- **Post-Training Quantization (PTQ)**: Quantize weights and activations to INT8 using representative calibration datasets (100–500 realistic domain samples).
- **Quantization-Aware Training (QAT)**: If PTQ accuracy drops $>1.5\%$, introduce fake-quantization nodes during fine-tuning.

### 3. Execution Providers & Memory Footprint
- Target hardware acceleration backends:
  - NVIDIA: **TensorRT Execution Provider** (`CUDAExecutionProvider` fallback).
  - Intel: **OpenVINO Execution Provider**.
  - ARM/Embedded: **NNAPI** or **XNNPACK**.
- Pre-allocate memory buffers and pin host memory (`cudaHostAlloc`) to avoid allocation overhead during real-time control loops.
- Set thermal profiles and power limits (e.g. `nvpmodel -m 0` on Jetson) for sustained robotics operation without throttling.

