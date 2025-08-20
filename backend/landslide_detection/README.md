### YOLOv8 training & testing for landslide detection (Roboflow dataset)

This module provides a simple CLI to train and evaluate YOLOv8 models using a Roboflow dataset or a local `data.yaml`.

#### 1) Install
```powershell
# From repo root
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend\landslide_detection\requirements.txt
```

#### 2) Download dataset from Roboflow and train
Set your Roboflow API key once per session:
```powershell
$env:ROBOFLOW_API_KEY = "<YOUR_API_KEY>"
```
Then run training + evaluation:
```powershell
python backend\landslide_detection\train_test_yolov8.py ^
  --roboflow-workspace trial-m86h3 ^
  --roboflow-project landslide-vwyie ^
  --roboflow-version 4 ^
  --model yolov8n.pt ^
  --epochs 50 ^
  --imgsz 640 ^
  --run-name rf_v4 ^
  --save-preds
```

You can also pass the API key directly via flag `--roboflow-api-key` instead of using the environment variable.

#### 3) Use an existing local dataset
If you already have a YOLO-format dataset with a `data.yaml`:
```powershell
python backend\landslide_detection\train_test_yolov8.py ^
  --data-yaml path\to\data.yaml ^
  --model yolov8n.pt ^
  --epochs 50 ^
  --imgsz 640 ^
  --run-name local_data ^
  --save-preds
```

#### Outputs
Results, metrics, and predictions are saved under `runs/landslide_yolov8/`. Two evaluations are performed automatically:
- Validation split: `val`
- Test split: `test` (if present in `data.yaml`)

To change hardware or batch size, use:
- `--device`: `auto`, `cpu`, `cuda`, or an index like `0`
- `--batch`: integer or `auto` (default)
