#!/usr/bin/env python3
"""
Lunar Image Processor - Single script for all image processing needs
Handles enhancement, zooming, and tiling with error handling
"""

import argparse
import json
import sys
import time
import warnings
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

warnings.filterwarnings('ignore')

# Default input directory for images on Windows
DEFAULT_INPUT_DIR = Path(r"D:\projects\website\input")

class LunarImageProcessor:
    def __init__(self):
        Image.MAX_IMAGE_PIXELS = None  # Remove PIL limit

    def enhance_image(self, img_array, method='all'):
        """Apply enhancement techniques to improve image quality"""
        try:
            enhanced = img_array.copy().astype(np.float32)

            if method in ['sharpen', 'all']:
                # Advanced unsharp masking
                gaussian = cv2.GaussianBlur(enhanced, (0, 0), 1.5)
                enhanced = cv2.addWeighted(enhanced, 1.8, gaussian, -0.8, 0)
                enhanced = np.clip(enhanced, 0, 255)

            if method in ['denoise', 'all']:
                # Non-local means denoising
                enhanced = cv2.fastNlMeansDenoising(
                    enhanced.astype(np.uint8),
                    h=10,
                    templateWindowSize=7,
                    searchWindowSize=21
                )
                enhanced = enhanced.astype(np.float32)

            if method in ['contrast', 'all']:
                # CLAHE contrast enhancement
                clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
                enhanced = clahe.apply(enhanced.astype(np.uint8)).astype(np.float32)

            return enhanced.astype(np.uint8)
        except Exception as e:
            print(f"❌ Enhancement failed: {e}")
            return img_array

    def super_resolution_upscale(self, img_array, scale_factor):
        """High-quality super-resolution upscaling"""
        try:
            height, width = img_array.shape[:2]
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)

            # Use INTER_CUBIC for initial upscaling
            upscaled = cv2.resize(img_array, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

            # Apply edge-preserving smoothing
            upscaled = cv2.edgePreservingFilter(upscaled, flags=2, sigma_s=50, sigma_r=0.4)

            # Additional sharpening for lunar terrain
            kernel = np.array([[-1,-1,-1], [-1, 9,-1], [-1,-1,-1]])
            upscaled = cv2.filter2D(upscaled, -1, kernel * 0.3)
            upscaled = np.clip(upscaled, 0, 255)

            return upscaled.astype(np.uint8)
        except Exception as e:
            print(f"❌ Upscaling failed: {e}")
            return img_array

    def lanczos_upscale(self, pil_img, scale_factor):
        """High-quality Lanczos upscaling"""
        try:
            width, height = pil_img.size
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            return pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        except Exception as e:
            print(f"❌ Lanczos upscaling failed: {e}")
            return pil_img

    def process_image(self, input_path, output_dir, zoom_factor=4, enhancement_factor=4,
                     tile_size=640, overlap=0.2, enhancement_method='all'):
        """Main processing function with comprehensive error handling"""

        try:
            print("="*60)
            print("🚀 LUNAR IMAGE PROCESSING STARTED")
            print("="*60)

            # Validate input
            if not Path(input_path).exists():
                raise FileNotFoundError(f"Input image not found: {input_path}")

            # Create output directory
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            # Load image
            print(f"📁 Loading image: {input_path}")
            img = Image.open(input_path)

            if img.mode != 'L':
                img = img.convert('L')  # Convert to grayscale for lunar images

            print(f"📏 Original dimensions: {img.width} x {img.height}")

            # Convert to numpy array
            img_array = np.array(img)

            # Step 1: Enhance image quality
            print(f"✨ Enhancing image quality using method: {enhancement_method}")
            enhanced_array = self.enhance_image(img_array, enhancement_method)

            # Step 2: Apply enhancement upscaling
            total_scale = zoom_factor * enhancement_factor
            print(f"🔍 Scaling: {enhancement_factor}x enhancement + {zoom_factor}x zoom = {total_scale}x total")

            if enhancement_factor > 1:
                print("🚀 Applying super-resolution upscaling...")
                enhanced_array = self.super_resolution_upscale(enhanced_array, enhancement_factor)

            # Step 3: Apply zoom factor
            enhanced_img = Image.fromarray(enhanced_array)
            if zoom_factor > 1:
                print("🔍 Applying final zoom...")
                enhanced_img = self.lanczos_upscale(enhanced_img, zoom_factor)

            # Step 4: Final enhancement pass
            print("✨ Applying final enhancement...")
            final_array = np.array(enhanced_img)
            final_array = self.enhance_image(final_array, 'sharpen')
            enhanced_img = Image.fromarray(final_array)

            final_width, final_height = enhanced_img.size
            print(f"📏 Final dimensions: {final_width} x {final_height}")

            # Step 5: Create tiles
            print("🧩 Creating tiles...")
            self._create_tiles(enhanced_img, output_dir, tile_size, overlap)

            # Step 6: Save metadata
            self._save_metadata(input_path, output_dir, zoom_factor, enhancement_factor,
                              total_scale, enhancement_method, img.size, (final_width, final_height))

            print("\n" + "="*60)
            print("🎉 PROCESSING COMPLETED SUCCESSFULLY!")
            print("="*60)
            print(f"📁 Output directory: {output_dir}")
            print(f"🔍 Total scaling applied: {total_scale}x")

            # Cleanup
            img.close()
            enhanced_img.close()

        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            print("💡 Check your input file and parameters")
            return False

        return True

    def _create_tiles(self, enhanced_img, output_dir, tile_size, overlap):
        """Create tiles with train/val/test split"""
        try:
            overlap_pixels = int(tile_size * overlap)
            stride = tile_size - overlap_pixels

            # Create output directories
            train_dir = output_dir / "train"
            val_dir = output_dir / "val"
            test_dir = output_dir / "test"

            for dir_path in [train_dir, val_dir, test_dir]:
                dir_path.mkdir(exist_ok=True)

            # Calculate tiles
            final_width, final_height = enhanced_img.size
            tiles_info = []

            for y in range(0, final_height, stride):
                for x in range(0, final_width, stride):
                    tile_w = min(tile_size, final_width - x)
                    tile_h = min(tile_size, final_height - y)

                    if tile_w >= tile_size * 0.5 and tile_h >= tile_size * 0.5:
                        tiles_info.append({
                            'x': x, 'y': y, 'width': tile_w, 'height': tile_h,
                            'row': y // stride, 'col': x // stride
                        })

            # Split tiles by rows to avoid data leakage
            rows = {}
            for tile in tiles_info:
                row = tile['row']
                if row not in rows:
                    rows[row] = []
                rows[row].append(tile)

            sorted_rows = sorted(rows.keys())
            total_rows = len(sorted_rows)

            train_end = int(total_rows * 0.7)
            val_end = train_end + int(total_rows * 0.15)

            train_tiles = []
            val_tiles = []
            test_tiles = []

            for i, row in enumerate(sorted_rows):
                if i < train_end:
                    train_tiles.extend(rows[row])
                elif i < val_end:
                    val_tiles.extend(rows[row])
                else:
                    test_tiles.extend(rows[row])

            print(f"📊 Total tiles: {len(tiles_info)} (Train: {len(train_tiles)}, Val: {len(val_tiles)}, Test: {len(test_tiles)})")

            # Process tiles
            self._process_tile_batch(train_tiles, train_dir, "training", enhanced_img, tile_size)
            self._process_tile_batch(val_tiles, val_dir, "validation", enhanced_img, tile_size)
            self._process_tile_batch(test_tiles, test_dir, "testing", enhanced_img, tile_size)

        except Exception as e:
            print(f"❌ Tile creation failed: {e}")
            raise

    def _process_tile_batch(self, tiles, output_subdir, split_name, enhanced_img, tile_size):
        """Process a batch of tiles"""
        try:
            print(f"🔄 Processing {split_name} tiles...")
            for i, tile in enumerate(tiles):
                if i % 50 == 0:
                    print(f"  📍 Progress: {i+1}/{len(tiles)} tiles")

                # Create filename
                filename = f"tile_{tile['row']:04d}_{tile['col']:04d}.png"
                output_path = output_subdir / filename

                # Crop tile
                box = (tile['x'], tile['y'], tile['x'] + tile['width'], tile['y'] + tile['height'])
                tile_img = enhanced_img.crop(box)

                # Apply light enhancement
                tile_array = np.array(tile_img)
                kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
                tile_array = cv2.filter2D(tile_array, -1, kernel * 0.2)
                tile_array = np.clip(tile_array, 0, 255)

                tile_img = Image.fromarray(tile_array.astype(np.uint8))

                # Pad to exact tile size if needed
                if tile_img.size != (tile_size, tile_size):
                    padded_tile = Image.new('L', (tile_size, tile_size), 0)
                    padded_tile.paste(tile_img, (0, 0))
                    padded_tile.save(output_path, 'PNG', optimize=True)
                else:
                    tile_img.save(output_path, 'PNG', optimize=True)

            print(f"✅ Completed {split_name}: {len(tiles)} tiles")

        except Exception as e:
            print(f"❌ {split_name} processing failed: {e}")
            raise

    def _save_metadata(self, input_path, output_dir, zoom_factor, enhancement_factor,
                       total_scale, enhancement_method, original_size, enhanced_size):
        """Save processing metadata"""
        try:
            metadata = {
                'input_image': str(input_path),
                'zoom_factor': zoom_factor,
                'enhancement_factor': enhancement_factor,
                'total_scale_factor': total_scale,
                'enhancement_method': enhancement_method,
                'original_dimensions': {'width': original_size[0], 'height': original_size[1]},
                'enhanced_dimensions': {'width': enhanced_size[0], 'height': enhanced_size[1]},
                'processing_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                'script_version': '1.0'
            }

            metadata_path = output_dir / "processing_metadata.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)

            print(f"📄 Metadata saved to: {metadata_path}")

        except Exception as e:
            print(f"⚠️  Metadata saving failed: {e}")

def get_user_choice():
    """Interactive menu for user to choose processing options"""
    print("\n" + "="*60)
    print("🎯 LUNAR IMAGE PROCESSING OPTIONS")
    print("="*60)
    print("Choose your processing configuration:")
    print()
    print("1️⃣  MAXIMUM QUALITY: 4x zoom + 4x enhancement = 16x total scaling")
    print("   💡 Best for boulder detection, maximum detail")
    print("   ⚠️  Requires significant memory and processing time")
    print()
    print("2️⃣  HIGH QUALITY: 3x zoom + 3x enhancement = 9x total scaling")
    print("   💡 Excellent detail with moderate resource usage")
    print()
    print("3️⃣  BALANCED: 2x zoom + 2x enhancement = 4x total scaling")
    print("   💡 Good quality, balanced performance")
    print()
    print("4️⃣  ZOOM ONLY: 4x zoom + 1x enhancement = 4x total scaling")
    print("   💡 Size increase without quality enhancement")
    print()
    print("5️⃣  ENHANCEMENT ONLY: 1x zoom + 4x enhancement = 4x total scaling")
    print("   💡 Quality improvement without size increase")
    print()
    print("6️⃣  CLEAN TILING: 1x zoom + 1x enhancement = 1x total scaling")
    print("   💡 Fastest processing, original resolution")
    print()
    print("7️⃣  CUSTOM: Choose your own zoom and enhancement factors")
    print()

    while True:
        try:
            choice = input("Enter your choice (1-7): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7']:
                return choice
            else:
                print("❌ Please enter a number between 1 and 7")
        except KeyboardInterrupt:
            print("\n⚠️  Exiting...")
            return None

def get_custom_factors():
    """Get custom zoom and enhancement factors from user"""
    print("\n🔧 CUSTOM CONFIGURATION")
    print("="*40)

    while True:
        try:
            zoom = int(input("Enter zoom factor (1-8): "))
            if 1 <= zoom <= 8:
                break
            else:
                print("❌ Zoom factor must be between 1 and 8")
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            return None, None

    while True:
        try:
            enhance = int(input("Enter enhancement factor (1-8): "))
            if 1 <= enhance <= 8:
                break
            else:
                print("❌ Enhancement factor must be between 1 and 8")
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            return None, None

    return zoom, enhance

def main():
    """Main function with interactive menu and argument parsing"""

    # Check if arguments were provided (command line mode)
    if len(sys.argv) > 1:
        # Command line mode
        parser = argparse.ArgumentParser(
            description='Process lunar images with enhancement, zooming, and tiling',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Maximum quality (4x zoom + 4x enhancement = 16x total)
  python process_lunar_images.py input.tif output_dir --zoom 4 --enhance 4
  
  # Moderate quality (2x zoom + 2x enhancement = 4x total)
  python process_lunar_images.py input.tif output_dir --zoom 2 --enhance 2
  
  # Zoom only (4x zoom, no enhancement)
  python process_lunar_images.py input.tif output_dir --zoom 4 --enhance 1
  
  # Clean tiling (no zoom, no enhancement)
  python process_lunar_images.py input.tif output_dir --zoom 1 --enhance 1
            """
        )

        parser.add_argument('input_image', help='Input TIFF image path')
        parser.add_argument('output_dir', help='Output directory for processed tiles')
        parser.add_argument('--zoom', '-z', type=int, default=4,
                           help='Zoom factor (default: 4)')
        parser.add_argument('--enhance', '-e', type=int, default=4,
                           help='Enhancement factor (default: 4)')
        parser.add_argument('--tile-size', '-t', type=int, default=640,
                           help='Tile size in pixels (default: 640)')
        parser.add_argument('--overlap', '-o', type=float, default=0.2,
                           help='Overlap ratio between tiles (default: 0.2)')
        parser.add_argument('--method', '-m', choices=['sharpen', 'denoise', 'contrast', 'all'],
                           default='all', help='Enhancement method (default: all)')

        args = parser.parse_args()

        # Allow passing just a filename; resolve against default input directory
        try:
            provided_path = Path(args.input_image)
            if not provided_path.exists():
                candidate = DEFAULT_INPUT_DIR / args.input_image
                if candidate.exists():
                    args.input_image = str(candidate)
        except Exception:
            pass

        # Validate arguments
        if args.zoom < 1 or args.enhance < 1:
            print("❌ Error: Zoom and enhancement factors must be >= 1")
            return 1

        if args.tile_size < 64:
            print("❌ Error: Tile size must be >= 64 pixels")
            return 1

        if not (0 <= args.overlap < 1):
            print("❌ Error: Overlap must be between 0 and 1")
            return 1

        zoom_factor = args.zoom
        enhancement_factor = args.enhance
        tile_size = args.tile_size
        overlap = args.overlap
        enhancement_method = args.method
        input_image = args.input_image
        output_dir = args.output_dir

    else:
        # Interactive mode
        print("🚀 LUNAR IMAGE PROCESSOR - INTERACTIVE MODE")
        print("="*50)

        # Get input file: try default directory first, then ask for full path
        default_dir = DEFAULT_INPUT_DIR
        print(f"Default input directory: {default_dir}")

        input_image = None
        # Only try default dir prompt if it exists
        if default_dir.exists() and default_dir.is_dir():
            image_name = input("Enter image file name in the default directory (e.g., myimage.tif). Press Enter to provide a full path instead: ").strip().strip('"')
            if image_name:
                candidate = default_dir / image_name
                if candidate.is_file():
                    input_image = str(candidate)
                else:
                    print(f"❌ Not found in default directory: {candidate}")

        # Fallback to asking for full path until a valid file is provided
        while not input_image:
            raw_path = input("Enter full input image path: ").strip().strip('"')
            if not raw_path:
                print("❌ Path cannot be empty. Please provide a valid image file path.")
                continue
            if Path(raw_path).is_file():
                input_image = raw_path
            else:
                print(f"❌ File not found: {raw_path}")
                print("💡 Please check the path and try again")

        # Get output directory
        output_dir = input("Enter output directory (default: enhanced_lunar_tiles): ").strip().strip('"')
        if not output_dir:
            output_dir = "enhanced_lunar_tiles"

        # Get processing choice
        choice = get_user_choice()
        if choice is None:
            return 1

        # Set factors based on choice
        if choice == '1':  # Maximum quality
            zoom_factor, enhancement_factor = 4, 4
            print("\n✅ Selected: MAXIMUM QUALITY (4x zoom + 4x enhancement = 16x total)")
        elif choice == '2':  # High quality
            zoom_factor, enhancement_factor = 3, 3
            print("\n✅ Selected: HIGH QUALITY (3x zoom + 3x enhancement = 9x total)")
        elif choice == '3':  # Balanced
            zoom_factor, enhancement_factor = 2, 2
            print("\n✅ Selected: BALANCED (2x zoom + 2x enhancement = 4x total)")
        elif choice == '4':  # Zoom only
            zoom_factor, enhancement_factor = 4, 1
            print("\n✅ Selected: ZOOM ONLY (4x zoom + 1x enhancement = 4x total)")
        elif choice == '5':  # Enhancement only
            zoom_factor, enhancement_factor = 1, 4
            print("\n✅ Selected: ENHANCEMENT ONLY (1x zoom + 4x enhancement = 4x total)")
        elif choice == '6':  # Clean tiling
            zoom_factor, enhancement_factor = 1, 1
            print("\n✅ Selected: CLEAN TILING (1x zoom + 1x enhancement = 1x total)")
        elif choice == '7':  # Custom
            zoom_factor, enhancement_factor = get_custom_factors()
            if zoom_factor is None or enhancement_factor is None:
                return 1
            total_scale = zoom_factor * enhancement_factor
            print(f"\n✅ Selected: CUSTOM ({zoom_factor}x zoom + {enhancement_factor}x enhancement = {total_scale}x total)")

        # Default values for other parameters
        tile_size = 640
        overlap = 0.2
        enhancement_method = 'all'

        # Ask for tile size
        tile_input = input(f"Enter tile size in pixels (default: {tile_size}): ").strip()
        if tile_input:
            try:
                tile_size = int(tile_input)
                if tile_size < 64:
                    print("⚠️  Tile size too small, using minimum of 64 pixels")
                    tile_size = 64
            except ValueError:
                print(f"⚠️  Invalid tile size, using default: {tile_size}")

        # Ask for overlap
        overlap_input = input(f"Enter overlap ratio 0.0-0.5 (default: {overlap}): ").strip()
        if overlap_input:
            try:
                overlap = float(overlap_input)
                if not (0 <= overlap <= 0.5):
                    print("⚠️  Overlap must be between 0.0 and 0.5, using default")
                    overlap = 0.2
            except ValueError:
                print(f"⚠️  Invalid overlap, using default: {overlap}")

    try:
        # Process the image
        processor = LunarImageProcessor()
        success = processor.process_image(
            input_image,
            output_dir,
            zoom_factor,
            enhancement_factor,
            tile_size,
            overlap,
            enhancement_method
        )

        return 0 if success else 1

    except KeyboardInterrupt:
        print("\n⚠️  Processing interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
