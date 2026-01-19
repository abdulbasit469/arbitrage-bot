import asyncio
import os
import logging
from pathlib import Path
import uvicorn
from contextlib import asynccontextmanager

# Ensure logs directory exists
Path("logs").mkdir(exist_ok=True)
Path("data").mkdir(exist_ok=True)

# Import Bot and Dashboard
from src.main import ArbitrageBot
from src.dashboard.app import DashboardApp

# Global bot instance
bot_instance = None

@asynccontextmanager
async def lifespan(app):
    # STARTUP: Launch the bot in the background
    print("🚀 Starting Arbitrage Bot + Dashboard...")
    global bot_instance
    try:
        # Initialize Bot
        bot_instance = ArbitrageBot()
        
        # Run Bot in background task
        # We use create_task to run it concurrently with the web server
        asyncio.create_task(bot_instance.run())
        print("✅ Bot background task started!")
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")
        import traceback
        traceback.print_exc()
    
    yield
    
    # SHUTDOWN: Cleanup
    print("🛑 Shutting down...")

# Initialize Dashboard with Lifespan
port = int(os.getenv("PORT", 8000))
dashboard = DashboardApp(db_path="data/arbitrage_events.db", port=port)
app = dashboard.get_app()

# Attach lifespan manager to the app
app.router.lifespan_context = lifespan

if __name__ == "__main__":
    # Run server
    uvicorn.run(app, host="0.0.0.0", port=port)
