# Lunar Image Processor

**Single script for all lunar image processing needs** - enhancement, zooming, and tiling with comprehensive error handling.

## 🚀 Quick Start

### Windows (Recommended)
```bash
run_processor.bat
```
This will process your image with **4x zoom + 4x enhancement = 16x total scaling**.

### Command Line
```bash
# Install dependencies
pip install -r requirements.txt

# Maximum quality (4x zoom + 4x enhancement = 16x total)
python process_lunar_images.py input.tif output_dir --zoom 4 --enhance 4

# Moderate quality (2x zoom + 2x enhancement = 4x total)
python process_lunar_images.py input.tif output_dir --zoom 2 --enhance 2

# Zoom only (4x zoom, no enhancement)
python process_lunar_images.py input.tif output_dir --zoom 4 --enhance 1

# Clean tiling (no zoom, no enhancement)
python process_lunar_images.py input.tif output_dir --zoom 1 --enhance 1
```

## 📁 What You Get

- **Enhanced Image Quality**: Sharpening, denoising, contrast enhancement
- **High-Quality Upscaling**: Super-resolution techniques for lunar terrain
- **Organized Tiles**: Train/validation/test split with overlap
- **Metadata**: Complete processing information and statistics
- **Error Handling**: Comprehensive error checking and recovery

## ⚙️ Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--zoom` | 4 | Zoom factor (1-8) |
| `--enhance` | 4 | Enhancement factor (1-8) |
| `--tile-size` | 640 | Tile size in pixels |
| `--overlap` | 0.2 | Overlap ratio (0.1-0.5) |
| `--method` | all | Enhancement method (sharpen/denoise/contrast/all) |

## 📊 Scaling Examples

- **16x Total**: `--zoom 4 --enhance 4` (Maximum detail for boulder detection)
- **4x Total**: `--zoom 2 --enhance 2` (Balanced quality and performance)
- **4x Zoom**: `--zoom 4 --enhance 1` (Size increase only)
- **1x Original**: `--zoom 1 --enhance 1` (Fastest processing)

## 🔧 Requirements

- Python 3.7+
- See `requirements.txt` for dependencies

## 📈 Output Structure

```
output_dir/
├── train/          # 70% of tiles
├── val/            # 15% of tiles  
├── test/           # 15% of tiles
└── processing_metadata.json
```

## 💡 Tips

- **For boulder detection**: Use 4x zoom + 4x enhancement
- **For testing**: Start with smaller factors (2x2)
- **Memory issues**: Reduce scaling factors or tile size
- **Fast processing**: Use zoom only or clean tiling

---

**Just run `run_processor.bat` for maximum quality processing!** 🚀
