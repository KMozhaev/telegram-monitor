import os
import logging
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional, List
from telegram_parser.parser import TelegramParser

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Telegram Post Parser API")

# Initialize parser with optional rate limit from environment
max_rpm = os.getenv("MAX_REQUESTS_PER_MINUTE")
parser = TelegramParser(
    api_id=os.getenv("API_ID"),
    api_hash=os.getenv("API_HASH"),
    phone=os.getenv("PHONE"),
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