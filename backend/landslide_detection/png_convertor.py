#!/usr/bin/env python3
"""
TIFF → PNG converter for lunar geospatial imagery.

- Default: produces a view-optimized PNG using percentile stretch (avoids black output)
- Data mode: preserves pixel values and bit depth where possible (uint16)
- Reads TIFF robustly (prefers tifffile; falls back to OpenCV IMREAD_UNCHANGED)
- Handles float/signed/large-integer data with safe conversions
- Supports selecting specific bands when TIFF has > 4 bands

Usage examples:
  python png_convertor.py input.tif output.png
  python png_convertor.py input.tif output.png --compression 3
  python png_convertor.py input_multiband.tif output.png --bands 1,2,3
  python png_convertor.py input.tif output.png --mode data
  python png_convertor.py input.tif output.png --mode display --clip 2,98
"""

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np

try:
    import tifffile  # type: ignore
    _HAS_TIFFFILE = True
except Exception:
    tifffile = None
    _HAS_TIFFFILE = False


def parse_band_indices(bands_arg: str) -> list:
    indices = []
    for token in bands_arg.split(','):
        token = token.strip()
        if not token:
            continue
        try:
            # Accept 1-based indices from user but convert to 0-based
            idx = int(token)
            if idx <= 0:
                raise ValueError
            indices.append(idx - 1)
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"Invalid band index '{token}'. Use comma-separated positive integers, e.g., 1,2,3"
            )
    if not indices:
        raise argparse.ArgumentTypeError("No valid band indices provided")
    return indices


def load_tiff_preserve_dtype(input_path: Path) -> tuple[np.ndarray, bool]:
    """Load TIFF as ndarray, returning (array, is_bgr_order).

    If OpenCV is used for multi-channel, returns True for BGR ordering.
    """
    if _HAS_TIFFFILE:
        try:
            arr = tifffile.imread(str(input_path))
            if arr is None:
                raise ValueError(f"Failed to read image: {input_path}")
            # Handle channels-first data (C,H,W) → (H,W,C)
            if arr.ndim == 3 and arr.shape[0] in (3, 4) and arr.shape[2] not in (3, 4):
                arr = np.transpose(arr, (1, 2, 0))
            return arr, False
        except Exception as tif_err:
            # Fallback to OpenCV if tifffile fails (e.g., requires imagecodecs for LZW)
            arr_cv = cv2.imread(str(input_path), cv2.IMREAD_UNCHANGED)
            if arr_cv is None:
                raise ValueError(
                    "Failed to read TIFF with tifffile and OpenCV. "
                    f"tifffile error: {tif_err}. If the TIFF is LZW-compressed, install 'imagecodecs' (e.g., 'pip install imagecodecs') and retry."
                )
            is_bgr_cv = arr_cv.ndim == 3 and arr_cv.shape[2] in (3, 4)
            return arr_cv, is_bgr_cv

    # Fallback to OpenCV
    arr = cv2.imread(str(input_path), cv2.IMREAD_UNCHANGED)
    if arr is None:
        raise ValueError(f"Failed to read image: {input_path}")
    # OpenCV loads color as BGR/BGRA
    is_bgr = arr.ndim == 3 and arr.shape[2] in (3, 4)
    return arr, is_bgr


def select_bands_if_needed(image: np.ndarray, bands: list | None) -> np.ndarray:
    if image.ndim == 2:
        return image
    if image.ndim != 3:
        raise ValueError("Unsupported image shape: expected 2D or 3D array")

    height, width, num_channels = image.shape

    if num_channels <= 4:
        return image

    # More than 4 channels → require band selection or default to first 3
    if bands is None:
        return image[:, :, :3]

    # Validate provided band indices
    if max(bands) >= num_channels:
        raise ValueError(
            f"Requested band index exceeds available channels (requested up to {max(bands)+1}, available {num_channels})"
        )
    # Stack bands along channel dim in provided order
    return np.dstack([image[:, :, b] for b in bands])


def percentile_stretch(image: np.ndarray, low: float = 2.0, high: float = 98.0) -> np.ndarray:
    """Scale image to uint8 using per-channel percentile stretch for display.

    - Ignores non-finite values
    - If vmin == vmax, outputs mid-gray 128 for that channel
    """
    image_f = image.astype(np.float64)
    if image.ndim == 2:
        finite = np.isfinite(image_f)
        if not np.any(finite):
            return np.zeros_like(image, dtype=np.uint8)
        vmin = np.percentile(image_f[finite], low)
        vmax = np.percentile(image_f[finite], high)
        if vmin == vmax:
            return np.full_like(image, 128, dtype=np.uint8)
        scaled = (image_f - vmin) / (vmax - vmin)
        scaled = np.clip(scaled, 0.0, 1.0)
        return (scaled * 255.0 + 0.5).astype(np.uint8)

    # HWC
    channels = image.shape[2]
    out = np.zeros((image.shape[0], image.shape[1], channels), dtype=np.uint8)
    for c in range(channels):
        band = image_f[:, :, c]
        finite = np.isfinite(band)
        if not np.any(finite):
            out[:, :, c] = 0
            continue
        vmin = np.percentile(band[finite], low)
        vmax = np.percentile(band[finite], high)
        if vmin == vmax:
            out[:, :, c] = 128
            continue
        scaled = (band - vmin) / (vmax - vmin)
        scaled = np.clip(scaled, 0.0, 1.0)
        out[:, :, c] = (scaled * 255.0 + 0.5).astype(np.uint8)
    return out


def convert_dtype_to_png_compatible(image: np.ndarray) -> tuple[np.ndarray, str]:
    """Convert array to a PNG-compatible dtype while preserving information.

    Returns (converted_image, note)
    note describes any lossy conversions performed ("" if none).
    """
    note = ""
    dtype = image.dtype

    # PNG supports uint8 and uint16. It does not support float or signed integer directly.
    if dtype == np.uint8 or dtype == np.uint16:
        return image, note

    if np.issubdtype(dtype, np.floating):
        finite_mask = np.isfinite(image)
        if not np.any(finite_mask):
            # No finite values; fall back to all zeros uint8
            return np.zeros_like(image, dtype=np.uint8), "All values were non-finite; saved as zeros (uint8)."

        finite_vals = image[finite_mask]
        vmin = float(np.min(finite_vals))
        vmax = float(np.max(finite_vals))
        if vmin == vmax:
            scaled = np.zeros_like(image, dtype=np.uint16)
        else:
            # Scale to full uint16 range to preserve detail
            scaled = np.zeros_like(image, dtype=np.float64)
            scaled[finite_mask] = (image[finite_mask] - vmin) / (vmax - vmin)
            scaled = np.clip(scaled, 0.0, 1.0)
            scaled = (scaled * 65535.0 + 0.5).astype(np.uint16)
        note = f"Float data scaled linearly to uint16 using range [{vmin}, {vmax}]."
        return scaled, note

    if np.issubdtype(dtype, np.signedinteger):
        # Shift signed 16/32 to unsigned 16 where possible
        if dtype == np.int16:
            shifted = (image.astype(np.int32) + 32768).astype(np.uint16)
            note = "int16 shifted by +32768 to uint16."
            return shifted, note
        # For larger widths, clip to uint16 range
        imin = int(np.min(image))
        imax = int(np.max(image))
        shifted = image.astype(np.int64) - imin
        if imax == imin:
            out = np.zeros_like(image, dtype=np.uint16)
        else:
            out = (shifted * (65535.0 / (imax - imin))).astype(np.uint16)
        note = f"Signed integer data scaled to uint16 using range [{imin}, {imax}]."
        return out, note

    if np.issubdtype(dtype, np.unsignedinteger):
        # Wider than 16-bit → clip to 16-bit
        if image.dtype.itemsize > 2:
            note = "Clipped/truncated to uint16 from wider unsigned integer."
            return np.clip(image, 0, 65535).astype(np.uint16), note

    # Fallback: convert to uint8 safely with clipping
    note = f"Converted from {dtype} to uint8 with clipping."
    return np.clip(image, 0, 255).astype(np.uint8), note


def save_png_lossless(image: np.ndarray, output_path: Path, compression: int = 3) -> None:
    compression = int(np.clip(compression, 0, 9))
    params = [cv2.IMWRITE_PNG_COMPRESSION, compression]
    ok = cv2.imwrite(str(output_path), image, params)
    if not ok:
        raise ValueError(f"Failed to write PNG: {output_path}")


def convert_tif_to_png(
    input_tif: Path,
    output_png: Path,
    compression: int = 3,
    bands: list | None = None,
    mode: str = "display",
    clip_low: float = 2.0,
    clip_high: float = 98.0,
) -> None:
    image, is_bgr = load_tiff_preserve_dtype(input_tif)
    image = select_bands_if_needed(image, bands)

    # If OpenCV read BGR for 3/4-channel images, convert to RGB/RGBA.
    if is_bgr and image.ndim == 3 and image.shape[2] == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    elif is_bgr and image.ndim == 3 and image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)

    note = ""
    if mode == "display":
        # Make a viewer-friendly PNG (uint8) via percentile stretch
        image_disp = percentile_stretch(image, low=clip_low, high=clip_high)
        save_png_lossless(image_disp, output_png, compression=compression)
    else:
        # Data-preserving PNG as much as PNG allows
        converted, note = convert_dtype_to_png_compatible(image)
        save_png_lossless(converted, output_png, compression=compression)

    if note:
        print(f"⚠️  Note: {note}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Convert a TIFF (GeoTIFF pixel data) to PNG. Default mode generates a view-optimized PNG using "
            "percentile stretch to avoid black output; use --mode data to preserve values."
        ),
    )
    parser.add_argument("input_tif", type=Path, help="Path to input .tif/.tiff image")
    parser.add_argument("output_png", type=Path, help="Path to output .png image")
    parser.add_argument(
        "--compression",
        type=int,
        default=3,
        help="PNG compression level 0-9 (lossless). Higher is smaller and slower (default: 3)",
    )
    parser.add_argument(
        "--bands",
        type=parse_band_indices,
        default=None,
        help="Comma-separated 1-based band indices to export if input has >4 bands (e.g., 1,2,3)",
    )
    parser.add_argument(
        "--mode",
        choices=["display", "data"],
        default="display",
        help="display: viewer-friendly stretch to uint8; data: preserve data values/bit depth (default: display)",
    )
    parser.add_argument(
        "--clip",
        type=str,
        default="2,98",
        help="Low,High percentiles for display stretch (e.g., 2,98). Only used in display mode.",
    )

    args = parser.parse_args(argv)

    input_path: Path = args.input_tif
    output_path: Path = args.output_png

    if not input_path.exists():
        print(f"❌ Input not found: {input_path}")
        return 1
    if input_path.suffix.lower() not in {".tif", ".tiff"}:
        print("⚠️  Input does not look like a TIFF; proceeding anyway.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Parse clip percentiles
    try:
        low_str, high_str = (args.clip.split(",") + ["", ""])[:2]
        clip_low = float(low_str)
        clip_high = float(high_str)
    except Exception:
        print("⚠️  Invalid --clip value, using default 2,98")
        clip_low, clip_high = 2.0, 98.0
    clip_low = float(np.clip(clip_low, 0.0, 50.0))
    clip_high = float(np.clip(clip_high, 50.0, 100.0))
    if clip_low >= clip_high:
        clip_low, clip_high = 2.0, 98.0

    try:
        convert_tif_to_png(
            input_tif=input_path,
            output_png=output_path,
            compression=args.compression,
            bands=args.bands,
            mode=args.mode,
            clip_low=clip_low,
            clip_high=clip_high,
        )
        print(f"✅ Saved PNG: {output_path}")
        return 0
    except Exception as exc:
        print(f"❌ Conversion failed: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())


