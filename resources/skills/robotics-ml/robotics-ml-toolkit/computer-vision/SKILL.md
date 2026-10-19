---
name: computer-vision
description: "Architect and implement real-time computer vision pipelines, camera calibration, feature extraction, object detection, and optical flow."
---

# Computer Vision & Image Processing Protocol

Use this skill when developing, debugging, or optimizing computer vision pipelines in Python/C++ using OpenCV, PyTorch, or torchvision.

## Core Pipelines & Standards

### 1. Camera Calibration & Intrinsics
- Calibrate camera distortion parameters using standard chessboard/charuco targets:
  \[
  \begin{bmatrix} u \\ v \\ 1 \end{bmatrix} = \begin{bmatrix} f_x & 0 & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} X_c \\ Y_c \\ Z_c \end{bmatrix}
  \]
- Always undistort image streams (`cv2.undistort` or `cv2.initUndistortRectifyMap`) before running metric spatial calculations or visual odometry.
- Store calibration matrices as versioned JSON/YAML artifacts alongside camera serial numbers.

### 2. Image Preprocessing & Color Spaces
- **Color Space Conversions**: Be vigilant about channel order (`cv2.imread` loads BGR; PyTorch/Pillow expect RGB).
- **Normalization**: Standardize input tensors using dataset statistics (e.g. ImageNet mean `[0.485, 0.456, 0.406]` and std `[0.229, 0.224, 0.225]`).
- **Aspect-Ratio Preservation**: Never blindly resize images for neural networks; use letterboxing with gray padding to avoid geometric distortion of target features.

### 3. Object Detection & Tracking
- Use Non-Maximum Suppression (NMS) with tuned IoU thresholds (typically 0.45–0.60) to eliminate redundant bounding boxes.
- For multi-object tracking, pair detections with Kalman Filter state estimation and Hungarian algorithm assignment (e.g., ByteTrack or BoT-SORT).
- Guard against ID switching when tracks occlude: integrate re-identification feature embeddings.

### 4. Edge Performance & Threading
- Decouple image capture from inference: run the video frame grabber in a dedicated thread to prevent camera buffer overflows and latency lag.
- Prefer GPU zero-copy memory transfers (`cv2.cuda_GpuMat` or direct PyTorch tensor mapping) when streaming to neural accelerators.
