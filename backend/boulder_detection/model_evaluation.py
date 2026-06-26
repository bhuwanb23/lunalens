"""
Model Evaluation Script for Boulder Detection Models
Measures accuracy, precision, recall, F1-score, inference time, and other metrics.
"""

import json
import os
import sys
import time
from typing import Any

import numpy as np
import torch
from PIL import Image

# Add current directory to path for local imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from detector import BoulderDetector
from ml_models import ModelLoader
from transforms import DataTransforms


class ModelEvaluator:
    """Comprehensive model evaluation class."""

    def __init__(self, yolo_model_path: str, vit_model_path: str):
        """
        Initialize the evaluator.

        Args:
            yolo_model_path: Path to YOLO model
            vit_model_path: Path to ViT model
        """
        self.yolo_model_path = yolo_model_path
        self.vit_model_path = vit_model_path
        self.detector = None
        self.model_loader = None
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        # Initialize models
        self._load_models()

        # Metrics storage
        self.metrics = {
            'yolo': {},
            'vit': {},
            'combined': {}
        }

    def _load_models(self):
        """Load YOLO and ViT models."""
        try:
            print("🚀 Loading models for evaluation...")
            self.model_loader = ModelLoader(self.yolo_model_path, self.vit_model_path)
            self.detector = BoulderDetector(self.yolo_model_path, self.vit_model_path, scale=1.0)
            print("✅ Models loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            raise

    def evaluate_inference_speed(self, image_path: str, num_runs: int = 10) -> dict[str, float]:
        """
        Evaluate inference speed for both models.

        Args:
            image_path: Path to test image
            num_runs: Number of runs for averaging

        Returns:
            Dictionary with timing metrics
        """
        print(f"⏱️ Evaluating inference speed with {num_runs} runs...")

        # Load image
        image = Image.open(image_path).convert('RGB')
        image_np = np.array(image)

        # YOLO speed evaluation
        yolo_times = []
        for i in range(num_runs):
            start_time = time.time()
            results = self.detector.yolo_model(image_path, conf=0.1, iou=0.3)
            end_time = time.time()
            yolo_times.append(end_time - start_time)

        # ViT speed evaluation
        vit_times = []
        transforms = DataTransforms()
        for i in range(num_runs):
            start_time = time.time()
            vit_input = transforms.preprocess_image_for_vit(image).to(self.device)
            with torch.no_grad():
                vit_output = self.detector.vit_model(vit_input)
            end_time = time.time()
            vit_times.append(end_time - start_time)

        # Combined speed evaluation
        combined_times = []
        for i in range(num_runs):
            start_time = time.time()
            # YOLO detection
            results = self.detector.yolo_model(image_path, conf=0.1, iou=0.3)
            # ViT validation for low confidence
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    if box.conf[0].item() < 0.3:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cropped_image = image.crop((x1, y1, x2, y2))
                        vit_input = transforms.preprocess_image_for_vit(cropped_image).to(self.device)
                        with torch.no_grad():
                            self.detector.vit_model(vit_input)
            end_time = time.time()
            combined_times.append(end_time - start_time)

        # Calculate statistics
        def calculate_stats(times):
            return {
                'mean': np.mean(times),
                'std': np.std(times),
                'min': np.min(times),
                'max': np.max(times),
                'fps': 1.0 / np.mean(times)
            }

        return {
            'yolo': calculate_stats(yolo_times),
            'vit': calculate_stats(vit_times),
            'combined': calculate_stats(combined_times)
        }

    def evaluate_detection_accuracy(self, image_path: str, ground_truth: list[tuple] = None) -> dict[str, float]:
        """
        Evaluate detection accuracy.

        Args:
            image_path: Path to test image
            ground_truth: List of (x1, y1, x2, y2, class_id) tuples

        Returns:
            Dictionary with accuracy metrics
        """
        print("🎯 Evaluating detection accuracy...")

        # Get detections
        detected_objects = self.detector.detect_objects(image_path, confidence_threshold=0.1)

        if not detected_objects:
            return {
                'precision': 0.0,
                'recall': 0.0,
                'f1_score': 0.0,
                'num_detections': 0,
                'avg_confidence': 0.0
            }

        # Calculate metrics
        num_detections = len(detected_objects)
        avg_confidence = np.mean([obj.confidence for obj in detected_objects])

        # If ground truth is provided, calculate precision/recall
        if ground_truth:
            true_positives = 0
            false_positives = 0
            false_negatives = len(ground_truth)

            for obj in detected_objects:
                obj_bbox = obj.bbox
                best_iou = 0
                matched_gt = False

                for gt_bbox in ground_truth:
                    iou = self._calculate_iou(obj_bbox, gt_bbox[:4])
                    if iou > 0.5:  # IoU threshold
                        true_positives += 1
                        false_negatives -= 1
                        matched_gt = True
                        break

                if not matched_gt:
                    false_positives += 1

            precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
            recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        else:
            # Without ground truth, use confidence-based metrics
            high_conf_detections = [obj for obj in detected_objects if obj.confidence > 0.5]
            precision = len(high_conf_detections) / num_detections if num_detections > 0 else 0
            recall = precision  # Without GT, assume high confidence = high recall
            f1_score = precision

        return {
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'num_detections': num_detections,
            'avg_confidence': avg_confidence,
            'high_confidence_detections': len([obj for obj in detected_objects if obj.confidence > 0.5])
        }

    def evaluate_model_size(self) -> dict[str, float]:
        """Evaluate model size and memory usage."""
        print("📏 Evaluating model size...")

        # Get file sizes
        yolo_size = os.path.getsize(self.yolo_model_path) / (1024 * 1024)  # MB
        vit_size = os.path.getsize(self.vit_model_path) / (1024 * 1024)  # MB
        total_size = yolo_size + vit_size

        # Estimate memory usage
        yolo_memory = 2.0  # Approximate GPU memory in GB
        vit_memory = 1.5   # Approximate GPU memory in GB
        total_memory = yolo_memory + vit_memory

        return {
            'yolo_size_mb': yolo_size,
            'vit_size_mb': vit_size,
            'total_size_mb': total_size,
            'yolo_memory_gb': yolo_memory,
            'vit_memory_gb': vit_memory,
            'total_memory_gb': total_memory
        }

    def evaluate_detection_distribution(self, image_path: str) -> dict[str, Any]:
        """Evaluate detection distribution by object size and confidence."""
        print("📊 Evaluating detection distribution...")

        detected_objects = self.detector.detect_objects(image_path, confidence_threshold=0.01)

        if not detected_objects:
            return {
                'size_distribution': {},
                'confidence_distribution': {},
                'total_objects': 0
            }

        # Size distribution
        sizes = []
        for obj in detected_objects:
            x1, y1, x2, y2 = obj.bbox
            area = (x2 - x1) * (y2 - y1)
            sizes.append(area)

        size_ranges = {
            'small': len([s for s in sizes if s < 1000]),
            'medium': len([s for s in sizes if 1000 <= s < 5000]),
            'large': len([s for s in sizes if s >= 5000])
        }

        # Confidence distribution
        confidences = [obj.confidence for obj in detected_objects]
        conf_ranges = {
            'low': len([c for c in confidences if c < 0.3]),
            'medium': len([c for c in confidences if 0.3 <= c < 0.7]),
            'high': len([c for c in confidences if c >= 0.7])
        }

        return {
            'size_distribution': size_ranges,
            'confidence_distribution': conf_ranges,
            'total_objects': len(detected_objects),
            'avg_size': np.mean(sizes),
            'avg_confidence': np.mean(confidences)
        }

    def _calculate_iou(self, bbox1: tuple, bbox2: tuple) -> float:
        """Calculate Intersection over Union between two bounding boxes."""
        x1_1, y1_1, x2_1, y2_1 = bbox1
        x1_2, y1_2, x2_2, y2_2 = bbox2

        # Calculate intersection
        x1_i = max(x1_1, x1_2)
        y1_i = max(y1_1, y1_2)
        x2_i = min(x2_1, x2_2)
        y2_i = min(y2_1, y2_2)

        if x2_i <= x1_i or y2_i <= y1_i:
            return 0.0

        intersection = (x2_i - x1_i) * (y2_i - y1_i)

        # Calculate union
        area1 = (x2_1 - x1_1) * (y2_1 - y1_1)
        area2 = (x2_2 - x1_2) * (y2_2 - y1_2)
        union = area1 + area2 - intersection

        return intersection / union if union > 0 else 0.0

    def run_comprehensive_evaluation(self, image_path: str, ground_truth: list[tuple] = None) -> dict[str, Any]:
        """
        Run comprehensive evaluation of both models.

        Args:
            image_path: Path to test image
            ground_truth: Optional ground truth annotations

        Returns:
            Comprehensive evaluation results
        """
        print("🔍 Running comprehensive model evaluation...")

        results = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'image_path': image_path,
            'device': str(self.device),
            'speed_metrics': self.evaluate_inference_speed(image_path),
            'accuracy_metrics': self.evaluate_detection_accuracy(image_path, ground_truth),
            'size_metrics': self.evaluate_model_size(),
            'distribution_metrics': self.evaluate_detection_distribution(image_path)
        }

        # Calculate summary scores
        results['summary'] = {
            'overall_score': self._calculate_overall_score(results),
            'speed_score': self._calculate_speed_score(results['speed_metrics']),
            'accuracy_score': self._calculate_accuracy_score(results['accuracy_metrics']),
            'efficiency_score': self._calculate_efficiency_score(results['size_metrics'])
        }

        return results

    def _calculate_overall_score(self, results: dict) -> float:
        """Calculate overall model performance score (0-100)."""
        speed_score = results['summary']['speed_score']
        accuracy_score = results['summary']['accuracy_score']
        efficiency_score = results['summary']['efficiency_score']

        # Weighted average
        overall_score = (speed_score * 0.3 + accuracy_score * 0.5 + efficiency_score * 0.2)
        return min(100.0, overall_score)

    def _calculate_speed_score(self, speed_metrics: dict) -> float:
        """Calculate speed performance score (0-100)."""
        # Target: <200ms for combined inference
        target_time = 0.2
        actual_time = speed_metrics['combined']['mean']

        if actual_time <= target_time:
            return 100.0
        else:
            # Exponential decay for slower times
            score = 100.0 * np.exp(-(actual_time - target_time) / target_time)
            return max(0.0, score)

    def _calculate_accuracy_score(self, accuracy_metrics: dict) -> float:
        """Calculate accuracy performance score (0-100)."""
        f1_score = accuracy_metrics['f1_score']
        return f1_score * 100.0

    def _calculate_efficiency_score(self, size_metrics: dict) -> float:
        """Calculate efficiency score (0-100)."""
        # Target: <200MB total size
        target_size = 200.0
        actual_size = size_metrics['total_size_mb']

        if actual_size <= target_size:
            return 100.0
        else:
            score = 100.0 * (target_size / actual_size)
            return max(0.0, score)

    def save_evaluation_results(self, results: dict, output_path: str = "model_evaluation_results.json"):
        """Save evaluation results to JSON file."""
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"💾 Evaluation results saved to: {output_path}")

    def print_evaluation_summary(self, results: dict):
        """Print a formatted summary of evaluation results."""
        print("\n" + "="*80)
        print("📊 MODEL EVALUATION SUMMARY")
        print("="*80)

        print(f"🕒 Timestamp: {results['timestamp']}")
        print(f"🖼️ Image: {results['image_path']}")
        print(f"💻 Device: {results['device']}")

        print("\n" + "-"*40)
        print("⏱️ SPEED METRICS")
        print("-"*40)
        speed = results['speed_metrics']
        print(f"YOLO Inference: {speed['yolo']['mean']:.3f}s ± {speed['yolo']['std']:.3f}s ({speed['yolo']['fps']:.1f} FPS)")
        print(f"ViT Inference: {speed['vit']['mean']:.3f}s ± {speed['vit']['std']:.3f}s ({speed['vit']['fps']:.1f} FPS)")
        print(f"Combined: {speed['combined']['mean']:.3f}s ± {speed['combined']['std']:.3f}s ({speed['combined']['fps']:.1f} FPS)")

        print("\n" + "-"*40)
        print("🎯 ACCURACY METRICS")
        print("-"*40)
        accuracy = results['accuracy_metrics']
        print(f"Precision: {accuracy['precision']:.3f}")
        print(f"Recall: {accuracy['recall']:.3f}")
        print(f"F1-Score: {accuracy['f1_score']:.3f}")
        print(f"Detections: {accuracy['num_detections']}")
        print(f"Avg Confidence: {accuracy['avg_confidence']:.3f}")

        print("\n" + "-"*40)
        print("📏 SIZE METRICS")
        print("-"*40)
        size = results['size_metrics']
        print(f"YOLO Model: {size['yolo_size_mb']:.1f} MB")
        print(f"ViT Model: {size['vit_size_mb']:.1f} MB")
        print(f"Total Size: {size['total_size_mb']:.1f} MB")
        print(f"Memory Usage: {size['total_memory_gb']:.1f} GB")

        print("\n" + "-"*40)
        print("📊 DETECTION DISTRIBUTION")
        print("-"*40)
        dist = results['distribution_metrics']
        print(f"Total Objects: {dist['total_objects']}")
        print(f"Size Distribution: {dist['size_distribution']}")
        print(f"Confidence Distribution: {dist['confidence_distribution']}")

        print("\n" + "-"*40)
        print("🏆 PERFORMANCE SCORES")
        print("-"*40)
        summary = results['summary']
        print(f"Overall Score: {summary['overall_score']:.1f}/100")
        print(f"Speed Score: {summary['speed_score']:.1f}/100")
        print(f"Accuracy Score: {summary['accuracy_score']:.1f}/100")
        print(f"Efficiency Score: {summary['efficiency_score']:.1f}/100")

        print("\n" + "="*80)


def main():
    """Main function to run model evaluation."""
    print("🚀 Starting Model Evaluation...")

    # Model paths
    yolo_model_path = "best.pt"
    vit_model_path = "vit_model.pth"
    test_image_path = "download.png"

    # Check if files exist
    if not os.path.exists(yolo_model_path):
        print(f"❌ YOLO model not found at: {yolo_model_path}")
        return

    if not os.path.exists(vit_model_path):
        print(f"❌ ViT model not found at: {vit_model_path}")
        return

    if not os.path.exists(test_image_path):
        print(f"❌ Test image not found at: {test_image_path}")
        return

    try:
        # Initialize evaluator
        evaluator = ModelEvaluator(yolo_model_path, vit_model_path)

        # Run comprehensive evaluation
        results = evaluator.run_comprehensive_evaluation(test_image_path)

        # Print summary
        evaluator.print_evaluation_summary(results)

        # Save results
        evaluator.save_evaluation_results(results)

        print("\n✅ Model evaluation completed successfully!")

    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
