"""
Simple dashboard server for Railway.
"""
import os
from pathlib import Path

# Ensure necessary directories exist
print("Script starting: Checking directories...")
Path("data").mkdir(exist_ok=True)
Path("logs").mkdir(exist_ok=True)
print("Directories created.")

# Import dashboard
print("Importing DashboardApp...")
try:
    from src.dashboard.app import DashboardApp
    print("Import successful.")
except Exception as e:
    print(f"FAILED to import DashboardApp: {e}")
    raise

# Initialize dashboard
print("Initializing DashboardApp...")
try:
    port_str = os.getenv("PORT", "8000")
    print(f"Using port: {port_str}")
    dashboard = DashboardApp(
        db_path="data/arbitrage_events.db",
        port=int(port_str)
    )
    print("DashboardApp initialized.")
except Exception as e:
    print(f"FAILED to init DashboardApp: {e}")
    raise

# Export app for uvicorn
app = dashboard.get_app()
print("FastAPI app exported successfully.")
