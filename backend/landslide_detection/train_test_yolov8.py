import argparse
import os
import sys
import warnings
from pathlib import Path

warnings.filterwarnings('ignore')


def ensure_packages_importable() -> None:
    """
    Ensure required third-party packages are importable, providing helpful
    guidance if they are missing. This avoids opaque ImportErrors later.
    """
    missing = []
    try:
        import ultralytics  # noqa: F401
    except Exception:
        missing.append("ultralytics")

    # roboflow is optional if --data-yaml is provided
    try:
        import roboflow  # noqa: F401
    except Exception:
        pass

    if missing:
        print(
            "Missing required packages: " + ", ".join(missing) +
            "\nInstall dependencies: pip install -r backend/landslide_detection/requirements.txt",
            file=sys.stderr,
        )
        sys.exit(1)


def resolve_device(device_arg: str) -> str:
    """Return a concrete device string acceptable to Ultralytics.

    - If the user passed an explicit device (not 'auto'), return it as-is.
    - If 'auto', choose '0' if CUDA is available, otherwise 'cpu'.
    """
    if device_arg and device_arg.lower() != "auto":
        return device_arg

    try:
        import torch  # type: ignore

        return "0" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"


def download_roboflow_dataset(api_key: str, workspace: str, project: str, version: int) -> Path:
    """
    Download a Roboflow dataset in YOLOv8 format and return the path to its data.yaml.
    """
    try:
        from roboflow import Roboflow
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "roboflow package is required to download datasets. Install it first: pip install roboflow"
        ) from exc

    rf = Roboflow(api_key=api_key)
    proj = rf.workspace(workspace).project(project)
    ds = proj.version(version).download("yolov8")
    dataset_root = Path(ds.location)
    data_yaml = dataset_root / "data.yaml"
    if not data_yaml.exists():  # pragma: no cover
        raise FileNotFoundError(f"data.yaml not found at {data_yaml}")
    return data_yaml


def train_model(
    model_name_or_path: str,
    data_yaml: Path,
    epochs: int,
    imgsz: int,
    batch: int | None,
    device: str,
    project_out: Path,
    run_name: str,
) -> "YOLO":
    from ultralytics import YOLO

    model = YOLO(model_name_or_path)
    # Allow 'auto' batch size by passing None to ultralytics (it will handle conservatively)
    train_kwargs = {
        "data": str(data_yaml),
        "epochs": epochs,
        "imgsz": imgsz,
        "project": str(project_out),
        "name": run_name,
        "device": device,
    }
    if batch is not None:
        train_kwargs["batch"] = batch

    # Optional hyperparameters if provided
    # These map directly to Ultralytics' train args
    # We read from environment variables set by argparse in main via os.environ fallback
    opt_map = {
        "patience": os.environ.get("ULTRA_PATIENCE"),
        "lr0": os.environ.get("ULTRA_LR0"),
        "lrf": os.environ.get("ULTRA_LRF"),
        "optimizer": os.environ.get("ULTRA_OPTIMIZER"),
        "momentum": os.environ.get("ULTRA_MOMENTUM"),
        "weight_decay": os.environ.get("ULTRA_WEIGHT_DECAY"),
        "warmup_epochs": os.environ.get("ULTRA_WARMUP_EPOCHS"),
        "degrees": os.environ.get("ULTRA_DEGREES"),
        "translate": os.environ.get("ULTRA_TRANSLATE"),
        "scale": os.environ.get("ULTRA_SCALE"),
        "shear": os.environ.get("ULTRA_SHEAR"),
        "perspective": os.environ.get("ULTRA_PERSPECTIVE"),
        "flipud": os.environ.get("ULTRA_FLIPUD"),
        "fliplr": os.environ.get("ULTRA_FLIPLR"),
        "hsv_h": os.environ.get("ULTRA_HSV_H"),
        "hsv_s": os.environ.get("ULTRA_HSV_S"),
        "hsv_v": os.environ.get("ULTRA_HSV_V"),
        "mosaic": os.environ.get("ULTRA_MOSAIC"),
        "mixup": os.environ.get("ULTRA_MIXUP"),
        "copy_paste": os.environ.get("ULTRA_COPY_PASTE"),
        "cos_lr": os.environ.get("ULTRA_COS_LR"),
    }
    for key, val in opt_map.items():
        if val is None or val == "":
            continue
        # Convert numeric types where appropriate
        try:
            if key in {"patience"}:
                train_kwargs[key] = int(val)
            elif key in {"cos_lr"}:
                train_kwargs[key] = val.lower() in {"1", "true", "yes", "y"}
            elif key in {"optimizer"}:
                train_kwargs[key] = val
            else:
                train_kwargs[key] = float(val)
        except Exception:
            # If conversion fails, pass raw string
            train_kwargs[key] = val

    model.train(**train_kwargs)
    return model


def evaluate_model(
    model: "YOLO",
    data_yaml: Path,
    imgsz: int,
    batch: int | None,
    device: str,
    project_out: Path,
    run_name_prefix: str,
) -> None:
    val_kwargs = {
        "data": str(data_yaml),
        "imgsz": imgsz,
        "device": device,
        "project": str(project_out),
    }
    if batch is not None:
        val_kwargs["batch"] = batch

    # Validation split
    model.val(split="val", name=f"{run_name_prefix}_val", **val_kwargs)
    # Test split (if defined in data.yaml)
    model.val(split="test", name=f"{run_name_prefix}_test", **val_kwargs)


def predict_on_split(
    model: "YOLO",
    data_yaml: Path,
    split_key: str,
    imgsz: int,
    conf: float,
    iou: float,
    augment: bool,
    device: str,
    project_out: Path,
    run_name_prefix: str,
) -> None:
    import yaml

    with open(data_yaml, encoding="utf-8") as f:
        data_cfg = yaml.safe_load(f)

    split_path = data_cfg.get(split_key)
    if not split_path:
        return

    # Resolve relative paths against the location of data.yaml
    split_path_resolved = Path(split_path)
    if not split_path_resolved.is_absolute():
        split_path_resolved = (data_yaml.parent / split_path_resolved).resolve()
    if not split_path_resolved.exists():
        return

    from ultralytics import YOLO  # noqa: F401  # ensure side-effects registered
    model.predict(
        source=str(split_path_resolved),
        imgsz=imgsz,
        conf=conf,
        iou=iou,
        augment=augment,
        device=device,
        project=str(project_out),
        name=f"{run_name_prefix}_{split_key}_preds",
        save=True,
        stream=False,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train and test YOLOv8 on a Roboflow dataset or a local data.yaml",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Dataset sources
    parser.add_argument("--data-yaml", type=Path, default=None,
                        help="Path to an existing YOLO data.yaml. If provided, Roboflow download is skipped.")
    parser.add_argument("--roboflow-api-key", type=str, default=os.environ.get("ROBOFLOW_API_KEY"),
                        help="Roboflow API key. Falls back to ROBOFLOW_API_KEY env var.")
    parser.add_argument("--roboflow-workspace", type=str, default=None, help="Roboflow workspace slug")
    parser.add_argument("--roboflow-project", type=str, default=None, help="Roboflow project slug")
    parser.add_argument("--roboflow-version", type=int, default=1, help="Roboflow project version")

    # Training/eval
    parser.add_argument("--model", type=str, default="yolov8n.pt", help="YOLOv8 model name or checkpoint path")
    parser.add_argument("--epochs", type=int, default=50, help="Training epochs")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size for training and validation")
    parser.add_argument("--batch", type=str, default="auto", help="Batch size (int) or 'auto'")
    parser.add_argument("--device", type=str, default="auto", help="Device to use: 'cpu', 'cuda', or index like '0'")
    parser.add_argument("--project-out", type=Path, default=Path("runs/landslide_yolov8"), help="Output directory")
    parser.add_argument("--run-name", type=str, default="train", help="Run name for logging")

    # Common training hyperparameters (optional; pass only if you want to override defaults)
    parser.add_argument("--patience", type=int, default=None, help="Early stopping patience (epochs)")
    parser.add_argument("--lr0", type=float, default=None, help="Initial learning rate")
    parser.add_argument("--lrf", type=float, default=None, help="Final OneCycleLR learning rate fraction")
    parser.add_argument("--optimizer", type=str, default=None, help="Optimizer (auto, SGD, Adam, AdamW, NAdam, RMSProp)")
    parser.add_argument("--momentum", type=float, default=None, help="Optimizer momentum (SGD) / beta1 (Adam)")
    parser.add_argument("--weight-decay", dest="weight_decay", type=float, default=None, help="Weight decay")
    parser.add_argument("--warmup-epochs", dest="warmup_epochs", type=float, default=None, help="Warmup epochs")
    parser.add_argument("--degrees", type=float, default=None, help="Rotation augmentation degrees")
    parser.add_argument("--translate", type=float, default=None, help="Translation augmentation fraction")
    parser.add_argument("--scale", type=float, default=None, help="Scale augmentation gain")
    parser.add_argument("--shear", type=float, default=None, help="Shear augmentation degrees")
    parser.add_argument("--perspective", type=float, default=None, help="Perspective augmentation fraction")
    parser.add_argument("--flipud", type=float, default=None, help="Flip up-down probability")
    parser.add_argument("--fliplr", type=float, default=None, help="Flip left-right probability")
    parser.add_argument("--hsv-h", dest="hsv_h", type=float, default=None, help="HSV-H augmentation fraction")
    parser.add_argument("--hsv-s", dest="hsv_s", type=float, default=None, help="HSV-S augmentation fraction")
    parser.add_argument("--hsv-v", dest="hsv_v", type=float, default=None, help="HSV-V augmentation fraction")
    parser.add_argument("--mosaic", type=float, default=None, help="Mosaic augmentation probability")
    parser.add_argument("--mixup", type=float, default=None, help="MixUp augmentation probability")
    parser.add_argument("--copy-paste", dest="copy_paste", type=float, default=None, help="Copy-paste augmentation probability")
    parser.add_argument("--cos-lr", dest="cos_lr", action="store_true", help="Use cosine LR schedule")

    # Prediction
    parser.add_argument("--save-preds", action="store_true", help="Save predictions for val/test splits")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold for predictions")
    parser.add_argument("--predict-iou", dest="predict_iou", type=float, default=0.70, help="NMS IoU threshold for predictions")
    parser.add_argument("--augment-predict", dest="augment_predict", action="store_true", help="Enable test-time augmentation for predictions")

    args = parser.parse_args()

    # Normalize batch argument
    if isinstance(args.batch, str) and args.batch.lower() == "auto":
        args.batch = None
    else:
        try:
            args.batch = int(args.batch) if args.batch is not None else None
        except ValueError:
            print("--batch must be an integer or 'auto'", file=sys.stderr)
            sys.exit(2)

    return args


def main() -> None:
    # Disable external loggers by default for a clean CLI experience
    os.environ.setdefault("WANDB_DISABLED", "true")

    ensure_packages_importable()
    args = parse_args()

    # Resolve dataset yaml
    if args.data_yaml is not None:
        data_yaml = args.data_yaml
        if not data_yaml.exists():
            print(f"--data-yaml not found: {data_yaml}", file=sys.stderr)
            sys.exit(2)
    else:
        # Require Roboflow parameters
        missing = [k for k, v in {
            "--roboflow-api-key": args.roboflow_api_key,
            "--roboflow-workspace": args.roboflow_workspace,
            "--roboflow-project": args.roboflow_project,
        }.items() if not v]
        if missing:
            print(
                "Missing Roboflow parameters: " + ", ".join(missing) +
                "\nEither provide them or pass --data-yaml to use a local dataset.",
                file=sys.stderr,
            )
            sys.exit(2)
        data_yaml = download_roboflow_dataset(
            api_key=args.roboflow_api_key,
            workspace=args.roboflow_workspace,
            project=args.roboflow_project,
            version=args.roboflow_version,
        )

    args.project_out.mkdir(parents=True, exist_ok=True)

    # Propagate optional hyperparameters via environment for train_model to pick up
    def set_env_if_present(env_key: str, val) -> None:
        if val is None:
            return
        os.environ[env_key] = str(val)

    set_env_if_present("ULTRA_PATIENCE", args.patience)
    set_env_if_present("ULTRA_LR0", args.lr0)
    set_env_if_present("ULTRA_LRF", args.lrf)
    set_env_if_present("ULTRA_OPTIMIZER", args.optimizer)
    set_env_if_present("ULTRA_MOMENTUM", args.momentum)
    set_env_if_present("ULTRA_WEIGHT_DECAY", args.weight_decay)
    set_env_if_present("ULTRA_WARMUP_EPOCHS", args.warmup_epochs)
    set_env_if_present("ULTRA_DEGREES", args.degrees)
    set_env_if_present("ULTRA_TRANSLATE", args.translate)
    set_env_if_present("ULTRA_SCALE", args.scale)
    set_env_if_present("ULTRA_SHEAR", args.shear)
    set_env_if_present("ULTRA_PERSPECTIVE", args.perspective)
    set_env_if_present("ULTRA_FLIPUD", args.flipud)
    set_env_if_present("ULTRA_FLIPLR", args.fliplr)
    set_env_if_present("ULTRA_HSV_H", args.hsv_h)
    set_env_if_present("ULTRA_HSV_S", args.hsv_s)
    set_env_if_present("ULTRA_HSV_V", args.hsv_v)
    set_env_if_present("ULTRA_MOSAIC", args.mosaic)
    set_env_if_present("ULTRA_MIXUP", args.mixup)
    set_env_if_present("ULTRA_COPY_PASTE", args.copy_paste)
    set_env_if_present("ULTRA_COS_LR", args.cos_lr)

    # Train
    model = train_model(
        model_name_or_path=args.model,
        data_yaml=data_yaml,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=resolve_device(args.device),
        project_out=args.project_out,
        run_name=args.run_name,
    )

    # Evaluate (val + test)
    evaluate_model(
        model=model,
        data_yaml=data_yaml,
        imgsz=args.imgsz,
        batch=args.batch,
        device=resolve_device(args.device),
        project_out=args.project_out,
        run_name_prefix=args.run_name,
    )

    # Optional: save predictions
    if args.save_preds:
        predict_on_split(
            model=model,
            data_yaml=data_yaml,
            split_key="val",
            imgsz=args.imgsz,
            conf=args.conf,
            iou=args.predict_iou,
            augment=args.augment_predict,
            device=resolve_device(args.device),
            project_out=args.project_out,
            run_name_prefix=args.run_name,
        )
        predict_on_split(
            model=model,
            data_yaml=data_yaml,
            split_key="test",
            imgsz=args.imgsz,
            conf=args.conf,
            iou=args.predict_iou,
            augment=args.augment_predict,
            device=resolve_device(args.device),
            project_out=args.project_out,
            run_name_prefix=args.run_name,
        )


if __name__ == "__main__":
    main()


