"""
Quick Model Metrics Evaluation
Simple script to get basic performance metrics for YOLOv8 and ViT models.
"""

import os
import time
import numpy as np
from PIL import Image
import torch

def get_model_metrics():
    """Get basic metrics for the models."""
    print("📊 Getting Model Metrics...")
    
    # Model paths
    yolo_path = "best.pt"
    vit_path = "vit_model.pth"
    test_image = "download.png"
    
    # Check if files exist
    if not all(os.path.exists(f) for f in [yolo_path, vit_path, test_image]):
        print("❌ Required files not found. Please ensure best.pt, vit_model.pth, and download.png exist.")
        return
    
    # 1. Model Size Metrics
    print("\n📏 MODEL SIZE METRICS:")
    print("-" * 30)
    
    yolo_size = os.path.getsize(yolo_path) / (1024 * 1024)  # MB
    vit_size = os.path.getsize(vit_path) / (1024 * 1024)    # MB
    total_size = yolo_size + vit_size
    
    print(f"YOLOv8 Model Size: {yolo_size:.1f} MB")
    print(f"ViT Model Size: {vit_size:.1f} MB")
    print(f"Total Model Size: {total_size:.1f} MB")
    
    # 2. Memory Usage Estimation
    print("\n💾 MEMORY USAGE ESTIMATION:")
    print("-" * 30)
    
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
    
    # Approximate memory usage
    yolo_memory = 2.0 if device.type == 'cuda' else 1.0  # GB
    vit_memory = 1.5 if device.type == 'cuda' else 0.8   # GB
    total_memory = yolo_memory + vit_memory
    
    print(f"YOLOv8 Memory: {yolo_memory:.1f} GB")
    print(f"ViT Memory: {vit_memory:.1f} GB")
    print(f"Total Memory: {total_memory:.1f} GB")
    
    # 3. Speed Metrics (if models can be loaded)
    try:
        print("\n⏱️ SPEED METRICS:")
        print("-" * 30)
        
        # Import and load models
        from ultralytics import YOLO
        import timm
        
        # Load YOLO
        yolo_model = YOLO(yolo_path)
        
        # Load ViT
        vit_model = timm.create_model('vit_base_patch16_224', pretrained=False, num_classes=2)
        vit_model.load_state_dict(torch.load(vit_path, map_location=device))
        vit_model.to(device)
        vit_model.eval()
        
        # Test inference speed
        image = Image.open(test_image).convert('RGB')
        
        # YOLO speed test
        yolo_times = []
        for i in range(5):
            start = time.time()
            results = yolo_model(test_image, conf=0.1, iou=0.3)
            end = time.time()
            yolo_times.append(end - start)
        
        # ViT speed test
        vit_times = []
        from transforms import DataTransforms
        transforms = DataTransforms()
        
        for i in range(5):
            start = time.time()
            vit_input = transforms.preprocess_image_for_vit(image).to(device)
            with torch.no_grad():
                vit_output = vit_model(vit_input)
            end = time.time()
            vit_times.append(end - start)
        
        # Combined speed test
        combined_times = []
        for i in range(5):
            start = time.time()
            # YOLO detection
            results = yolo_model(test_image, conf=0.1, iou=0.3)
            # ViT validation for low confidence
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    if box.conf[0].item() < 0.3:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cropped_image = image.crop((x1, y1, x2, y2))
                        vit_input = transforms.preprocess_image_for_vit(cropped_image).to(device)
                        with torch.no_grad():
                            vit_model(vit_input)
            end = time.time()
            combined_times.append(end - start)
        
        print(f"YOLOv8 Inference: {np.mean(yolo_times):.3f}s ± {np.std(yolo_times):.3f}s")
        print(f"ViT Inference: {np.mean(vit_times):.3f}s ± {np.std(vit_times):.3f}s")
        print(f"Combined Inference: {np.mean(combined_times):.3f}s ± {np.std(combined_times):.3f}s")
        print(f"YOLOv8 FPS: {1.0/np.mean(yolo_times):.1f}")
        print(f"ViT FPS: {1.0/np.mean(vit_times):.1f}")
        print(f"Combined FPS: {1.0/np.mean(combined_times):.1f}")
        
    except Exception as e:
        print(f"❌ Speed test failed: {e}")
    
    # 4. Detection Metrics
    try:
        print("\n🎯 DETECTION METRICS:")
        print("-" * 30)
        
        from detector import BoulderDetector
        
        detector = BoulderDetector(yolo_path, vit_path, scale=1.0)
        
        # Test different confidence thresholds
        confidence_levels = [0.1, 0.3, 0.5, 0.7]
        
        for conf in confidence_levels:
            detected_objects = detector.detect_objects(test_image, confidence_threshold=conf)
            num_detections = len(detected_objects)
            avg_confidence = np.mean([obj.confidence for obj in detected_objects]) if detected_objects else 0
            
            print(f"Confidence {conf}: {num_detections} detections, avg confidence: {avg_confidence:.3f}")
        
        # Enhanced detection test
        enhanced_objects = detector.detect_with_enhanced_sensitivity(test_image)
        print(f"Enhanced Detection: {len(enhanced_objects)} detections")
        
    except Exception as e:
        print(f"❌ Detection test failed: {e}")
    
    # 5. Model Architecture Info
    print("\n🏗️ MODEL ARCHITECTURE:")
    print("-" * 30)
    
    try:
        # YOLO info
        yolo_model = YOLO(yolo_path)
        print(f"YOLO Model Type: {type(yolo_model).__name__}")
        print(f"YOLO Classes: {yolo_model.names}")
        
        # ViT info
        vit_model = timm.create_model('vit_base_patch16_224', pretrained=False, num_classes=2)
        print(f"ViT Model Type: {type(vit_model).__name__}")
        print(f"ViT Parameters: {sum(p.numel() for p in vit_model.parameters()):,}")
        
    except Exception as e:
        print(f"❌ Architecture info failed: {e}")
    
    # 6. Performance Summary
    print("\n📈 PERFORMANCE SUMMARY:")
    print("-" * 30)
    
    # Calculate scores
    size_score = max(0, 100 - (total_size - 200) * 0.5)  # Target: <200MB
    speed_score = max(0, 100 - (np.mean(combined_times) - 0.2) * 500) if 'combined_times' in locals() else 50
    detection_score = min(100, len(enhanced_objects) * 2) if 'enhanced_objects' in locals() else 50
    
    print(f"Size Score: {size_score:.1f}/100")
    print(f"Speed Score: {speed_score:.1f}/100")
    print(f"Detection Score: {detection_score:.1f}/100")
    
    overall_score = (size_score * 0.2 + speed_score * 0.3 + detection_score * 0.5)
    print(f"Overall Score: {overall_score:.1f}/100")
    
    # Performance rating
    if overall_score >= 80:
        rating = "🟢 EXCELLENT"
    elif overall_score >= 60:
        rating = "🟡 GOOD"
    elif overall_score >= 40:
        rating = "🟠 FAIR"
    else:
        rating = "🔴 NEEDS IMPROVEMENT"
    
    print(f"Performance Rating: {rating}")


if __name__ == "__main__":
    get_model_metrics() 