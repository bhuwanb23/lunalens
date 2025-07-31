from qgis_setup import initialize_qgis, get_qgis_app, cleanup_qgis

try:
    print("Initializing QGIS...")
    qgis_setup = initialize_qgis()  # You can pass your QGIS path if needed
    qgs_app = get_qgis_app()
    print("QGIS initialized successfully!")
except Exception as e:
    print("QGIS setup failed:", e)
finally:
    try:
        cleanup_qgis()
        print("QGIS cleaned up.")
    except Exception:
        pass