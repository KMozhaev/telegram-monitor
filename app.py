import os
import logging
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
from datetime import datetime
from telegram_parser.parser import TelegramParser
from dotenv import load_dotenv  # Add this import

# Load environment variables from .env file
load_dotenv()  # Add this line

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Telegram Post Parser API")

# Check if API credentials are loaded
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
phone = os.getenv("PHONE")
session_string = os.getenv("SESSION_STRING")

# Log credential status (without revealing actual values)
logger.info(f"API_ID: {'Not set' if not api_id else 'Set'}")
logger.info(f"API_HASH: {'Not set' if not api_hash else 'Set'}")
logger.info(f"PHONE: {'Not set' if not phone else 'Set'}")
logger.info(f"SESSION_STRING: {'Not set' if not session_string else 'Set'}")

# Initialize parser with string session from environment
max_rpm = os.getenv("MAX_REQUESTS_PER_MINUTE")
parser = TelegramParser(
    api_id=api_id,
    api_hash=api_hash,
    phone=phone,
    session_string=session_string
)
if max_rpm and max_rpm.isdigit():
    parser.max_requests_per_minute = int(max_rpm)

@app.get("/api/posts")
async def get_posts(
    channels: str = Query(..., description="Comma-separated list of channel usernames"),
    limit: int = Query(10, description="Maximum posts per channel"),
    days_back: Optional[int] = Query(None, description="Only posts from the last X days")
):
    """Get posts from specified Telegram channels with anti-blocking measures"""
    try:
        # Clean channel names (remove @ if present)
        channel_list = [c.strip().lstrip('@') for c in channels.split(",")]
        
        # Check for valid limit to avoid abuse
        if limit > 50:
            limit = 50
            logger.warning(f"Requested limit too high, capped at {limit}")
        
        posts = await parser.get_posts(channel_list, limit, days_back)
        
        return {
            "posts": posts,
            "meta": {
                "channels_processed": len(channel_list),
                "total_posts": len(posts),
                "retrieved_at": datetime.now().isoformat()
            }
        }
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "message": str(e)}
        )

@app.get("/api/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "ok", "version": "1.0.0"}