import sys
import os
import numpy as np

# QGIS setup
QGIS_PREFIX_PATH = r"C:\Program Files\QGIS 3.44.1"
os.environ["QGIS_PREFIX_PATH"] = QGIS_PREFIX_PATH
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(QGIS_PREFIX_PATH, "qt5", "plugins")
os.environ["PATH"] += ";" + os.path.join(QGIS_PREFIX_PATH, "bin")
os.environ["PATH"] += ";" + os.path.join(QGIS_PREFIX_PATH, "lib")
QGIS_PYTHON_PATH = os.path.join(QGIS_PREFIX_PATH, "python")
if QGIS_PYTHON_PATH not in sys.path:
    sys.path.insert(0, QGIS_PYTHON_PATH)

from qgis.core import QgsApplication, QgsRasterLayer, QgsProject

qgs = QgsApplication([], False)
qgs.setPrefixPath(QGIS_PREFIX_PATH, True)
qgs.initQgis()

def compute_curvatures(elevation, cellsize=1.0):
    # First and second derivatives
    dzdx = np.gradient(elevation, axis=1) / cellsize
    dzdy = np.gradient(elevation, axis=0) / cellsize
    d2zdx2 = np.gradient(dzdx, axis=1) / cellsize
    d2zdy2 = np.gradient(dzdy, axis=0) / cellsize
    d2zdxdy = np.gradient(dzdx, axis=0) / cellsize

    # Slope and aspect
    p = dzdx
    q = dzdy
    r = d2zdx2
    s = d2zdxdy
    t = d2zdy2
    grad2 = p**2 + q**2
    grad = np.sqrt(grad2)
    denom = (1 + grad2)
    denom_sqrt = np.sqrt(denom)

    # Profile curvature (in the direction of steepest slope)
    profile_curv = -(r * p**2 + 2 * s * p * q + t * q**2) / (grad2 * denom_sqrt + 1e-10)
    # Plan curvature (perpendicular to slope direction)
    plan_curv = (r * q**2 - 2 * s * p * q + t * p**2) / (grad2 * denom_sqrt + 1e-10)
    # General curvature (Gaussian curvature)
    gaussian_curv = (r * t - s**2) / (denom**2 + 1e-10)
    # Tangential curvature (combination)
    tangential_curv = plan_curv
    # Mean curvature (average of principal curvatures)
    mean_curv = 0.5 * (r + t) / (denom_sqrt**3 + 1e-10)

    return {
        'profile': profile_curv,
        'plan': plan_curv,
        'gaussian': gaussian_curv,
        'tangential': tangential_curv,
        'mean': mean_curv
    }

class CurvatureStats:
    def __init__(self):
        self.project = QgsProject.instance()
        self.layers = {}

    def load_tif(self, tif_path, layer_name="Raster"):
        raster_layer = QgsRasterLayer(tif_path, layer_name)
        if not raster_layer.isValid():
            print(f"❌ Failed to load raster: {tif_path}")
            return None
        self.project.addMapLayer(raster_layer)
        self.layers[layer_name] = raster_layer
        print(f"✅ Loaded raster: {tif_path}")
        return raster_layer

    def compute_and_print_curvatures(self, layer_name="Raster"):
        if layer_name not in self.layers:
            print(f"❌ Layer '{layer_name}' not found.")
            return None
        layer = self.layers[layer_name]
        provider = layer.dataProvider()
        width = layer.width()
        height = layer.height()
        # Read a manageable block for demonstration (e.g., 1000x1000 or less)
        sample_width = min(width, 1000)
        sample_height = min(height, 1000)
        block = provider.block(1, layer.extent(), sample_width, sample_height)
        block_width = block.width()
        block_height = block.height()
        raw_data = np.array(block.data(), copy=False)

        if raw_data.size == block_width * block_height:
            data = raw_data.reshape((block_height, block_width))
        elif raw_data.ndim == 2 and raw_data.shape == (block_height, block_width):
            data = raw_data
        else:
            print(f"❌ Data shape mismatch: got {raw_data.shape}, expected ({block_height}, {block_width})")
            print(f"   - raw_data.size: {raw_data.size}")
            print(f"   - block_width: {block_width}, block_height: {block_height}")
            # Fallback: use as much as possible, or skip
            min_size = min(raw_data.size, block_width * block_height)
            data = np.zeros((block_height, block_width), dtype=raw_data.dtype)
            data.flat[:min_size] = raw_data.flat[:min_size]
            print("   - Used fallback zero-padded array.")

        elevation = data.astype(float)
        curvs = compute_curvatures(elevation)
        print("\n🌑 Curvature Statistics (Lunar DEM):")
        print("1. Profile Curvature: Curvature in the direction of the steepest slope (vertical plane). Affects flow acceleration/deceleration of landslides or debris.")
        print(f"   - Mean: {np.mean(curvs['profile']):.6f}, Std: {np.std(curvs['profile']):.6f}")
        print("2. Plan Curvature: Curvature perpendicular to the slope direction (horizontal plane). Controls flow divergence/convergence; useful for regolith paths.")
        print(f"   - Mean: {np.mean(curvs['plan']):.6f}, Std: {np.std(curvs['plan']):.6f}")
        print("3. General Curvature (Gaussian): Overall shape (spherical or Gaussian curvature). Describes local convexity/concavity.")
        print(f"   - Mean: {np.mean(curvs['gaussian']):.6f}, Std: {np.std(curvs['gaussian']):.6f}")
        print("4. Tangential Curvature: Combination of plan/profile. Useful for compound terrain interpretation.")
        print(f"   - Mean: {np.mean(curvs['tangential']):.6f}, Std: {np.std(curvs['tangential']):.6f}")
        print("5. Mean Curvature: Average of maximum and minimum curvatures. Useful in advanced geomorphology or simulation modeling.")
        print(f"   - Mean: {np.mean(curvs['mean']):.6f}, Std: {np.std(curvs['mean']):.6f}")
        return curvs

    def cleanup(self):
        qgs.exitQgis()
        print("✅ QGIS cleanup completed")

def main():
    tif_path = r"E:\moon extract\data\derived\20250207\ch2_tmc_ndn_20250207T1457348573_d_dtm_d18.tif"
    stats = CurvatureStats()
    stats.load_tif(tif_path, "Moon_DEM")
    stats.compute_and_print_curvatures("Moon_DEM")
    stats.cleanup()

if __name__ == "__main__":
    main()