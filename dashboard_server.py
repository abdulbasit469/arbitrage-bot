"""
Simple dashboard server for Railway.
"""
import os
from pathlib import Path

# Ensure necessary directories exist
Path("data").mkdir(exist_ok=True)
Path("logs").mkdir(exist_ok=True)

# Import dashboard
from src.dashboard.app import DashboardApp

# Initialize dashboard
dashboard = DashboardApp(
    db_path="data/arbitrage_events.db",
    port=int(os.getenv("PORT", 8000))
)

# Export app for uvicorn
app = dashboard.get_app()
