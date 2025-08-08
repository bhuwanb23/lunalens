# 🪨 Lunar Boulder Detection Suite

<div align="center">

![Boulder Detection](https://img.shields.io/badge/Boulder-Detection-orange?style=for-the-badge&logo=rocket)
![YOLO](https://img.shields.io/badge/YOLO-v8-red?style=for-the-badge&logo=yolo)
![Vision Transformer](https://img.shields.io/badge/ViT-Transformer-blue?style=for-the-badge&logo=transformer)
![Grad-CAM](https://img.shields.io/badge/Grad--CAM-Visualization-purple?style=for-the-badge&logo=eye)
![Python](https://img.shields.io/badge/Python-3.9%2B-green?style=for-the-badge&logo=python)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-orange?style=for-the-badge&logo=pytorch)

<br/>

<div style="background: linear-gradient(45deg, #ff6b35, #f7931e); padding: 16px; border-radius: 12px; margin: 16px 0; color: #fff;">

### 🚀 Advanced Lunar Boulder Detection
A production-ready toolkit for detecting and analyzing lunar boulders in images using YOLOv8 and Vision Transformer, with clean visualizations and built-in evaluation utilities.

</div>

</div>

---

## 🌟 Highlights

<div style="background: linear-gradient(135deg, #667eea, #764ba2); padding: 14px; border-radius: 10px; margin: 12px 0; color: #fff;">

- **Enhanced Detection Pipeline**: Multi-strategy YOLO inference (multi-threshold + IoU) with NMS-style merging and a small-object recovery pass for higher recall.
- **Clean Visual Output**: Bounding-box-only overlays by default (no cluttering labels) for publication-ready imagery.
- **Physical Measurements**: Width/height, area, diameter, volume, circularity, elongation; optional shadow-based depth estimation (experimental).
- **Grad-CAM & Attention**: YOLO Grad-CAM overlays; ViT uses a robust fallback attention map for interpretability.
- **Built-in Metrics**: Quick speed/size/detection counts and comprehensive evaluation (precision/recall/F1 if GT provided) with JSON reports.

</div>

---

## 🛠️ Installation

<div style="background: linear-gradient(45deg, #4facfe, #00f2fe); padding: 14px; border-radius: 10px; margin: 12px 0;">

1) Install dependencies

```bash
pip install -r requirements.txt
```

2) Place models in `backend/boulder_detection/`
- `best.pt` (YOLOv8 weights)
- `vit_model.pth` (ViT `vit_base_patch16_224` weights)

3) Verify environment

```bash
python backend/boulder_detection/test_imports.py
```

</div>

---

## 📁 Project Structure (core)

```
boulder_detection/
├─ detector.py              # Main detection logic + enhanced pipeline
├─ gradcam.py               # Grad-CAM & attention visualizations
├─ ml_models.py             # Model loading (YOLOv8, ViT)
├─ transforms.py            # Preprocessing for YOLO/ViT
├─ measurements.py          # Physical metrics & density
├─ main.py                  # Interactive CLI runner
├─ quick_metrics.py         # Lightweight speed/size/detection metrics
├─ model_evaluation.py      # Comprehensive evaluation + JSON report
├─ test_enhanced_detection.py
├─ test_clean_visualization.py
├─ best.pt                  # YOLO model weights (user-provided)
├─ vit_model.pth            # ViT weights (user-provided)
└─ download.png             # Example image
```

---

## ⚡ Quick Start

Run the interactive CLI (uses `download.png` in the same folder):

```bash
python -m boulder_detection.main
```

Programmatic usage:

```python
from boulder_detection import BoulderDetector

# Initialize
detector = BoulderDetector(
    yolo_model_path="best.pt",
    vit_model_path="vit_model.pth",
    scale=1.0  # meters per pixel
)

# 1) High-recall detection (enhanced pipeline)
objects = detector.detect_with_enhanced_sensitivity("download.png")

# 2) Standard YOLO detection with lower conf threshold (tunable)
objects_lowconf = detector.detect_objects("download.png", confidence_threshold=0.1)

# 3) YOLO + ViT fallback for low-confidence boxes
objects_vit = detector.detect_with_vit_fallback("download.png", confidence_threshold=0.3)

# Create clean visualization (boxes only)
viz_bgr = detector.create_visualization("download.png", objects)
```

---

## 🧠 Key Components

- `BoulderDetector` (in `detector.py`)
  - `detect_objects(image_path, confidence_threshold=0.1)`
  - `detect_with_vit_fallback(image_path, confidence_threshold=0.3)`
  - `detect_with_enhanced_sensitivity(image_path)`
  - `create_visualization(image_path, detected_objects)` → BGR image with bounding boxes only
  - `calculate_density_analysis(detected_objects, image_path)`
  - `print_detection_summary(detected_objects, density)`

- `GradCAMVisualizer` (in `gradcam.py`)
  - YOLO Grad-CAM (auto target layer)
  - ViT fallback attention map (robust alternative to Grad-CAM)

- `PhysicalCalculator` (in `measurements.py`)
  - Basic/shape metrics, volume estimation, optional depth estimation (experimental)

- `ModelLoader` (in `ml_models.py`)
  - Loads YOLOv8 and ViT; exposes device selection (CPU/GPU)

---

## 📊 Built-in Metrics & Evaluation

- Quick metrics (size, memory estimate, speed, detection counts):

```bash
python backend/boulder_detection/quick_metrics.py
```

- Comprehensive evaluation (speed, precision/recall/F1 if GT provided, distributions) + JSON:

```bash
python backend/boulder_detection/model_evaluation.py
# Outputs model_evaluation_results.json
```

Ground-truth for evaluation (optional) is expected as a list of `(x1, y1, x2, y2, class_id)` tuples; see `ModelEvaluator.evaluate_detection_accuracy`.

---

## 🎨 Visualizations

- Detection overlays are intentionally minimalist: only green bounding boxes for clarity.
- Grad-CAM: YOLO heatmaps are supported; ViT uses a reliable attention-map fallback.

> Tip: Save BGR output from `create_visualization` directly with OpenCV `cv2.imwrite`.

---

## ⚙️ Notes & Recommendations

- Models are expected in this folder as `best.pt` and `vit_model.pth`.
- The YOLO class-to-name mapping is handled internally; ensure your training classes align with your use-case. The sample setup treats the primary class as boulders.
- CPU works, but a CUDA GPU is recommended for speed (ViT is large).
- Tune `confidence_threshold` and IoU values for your imagery; the enhanced pipeline covers multiple thresholds and adds a small-object pass for improved recall.

---

## 🧪 Helpful Scripts

- `test_enhanced_detection.py`: compares original vs enhanced detection and saves comparison images.
- `test_clean_visualization.py`: verifies bounding-box-only visualization.
- `quick_metrics.py`: reports model size, speed, and detection counts at various thresholds.
- `model_evaluation.py`: runs a comprehensive benchmark and saves a JSON report.

---

## 🔧 Troubleshooting

<div style="background: linear-gradient(45deg, #ff6b6b, #ee5a24); padding: 12px; border-radius: 10px; margin: 12px 0; color: #fff;">

- Missing models: ensure `best.pt` and `vit_model.pth` exist.
- CPU too slow: switch to CUDA, reduce image size, or disable Grad-CAM.
- Memory pressure: close notebooks, reduce batch sizes, or move to GPU with more VRAM.
- Grad-CAM errors: install `grad-cam` (`pip install grad-cam`) and ensure compatible torch/ultralytics versions.

</div>

---

## 📄 License & Acknowledgments

- Licensed under MIT (see `LICENSE`).
- Powered by Ultralytics YOLOv8, ViT (timm), PyTorch, OpenCV, and Grad-CAM.

<div align="center" style="margin-top:12px;">

**🪨 Happy Boulder Detection!** ✨

</div> 