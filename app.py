import os
from fastapi import FastAPI
from fastapi import Query
from typing import Optional
from telegram_parser.parser import TelegramParser

app = FastAPI(title="Telegram Post Parser API")
parser = TelegramParser(
    api_id=os.getenv("API_ID"),
    api_hash=os.getenv("API_HASH"),
    phone=os.getenv("PHONE")
)

@app.get("/api/posts")
async def get_posts(
    channels: str = Query(..., description="Comma-separated list of channel usernames"),
    limit: int = Query(10, description="Maximum posts per channel"),
    days_back: Optional[int] = Query(None, description="Only posts from the last X days")
):
    channel_list = [c.strip() for c in channels.split(",")]
    posts = await parser.get_posts(channel_list, limit, days_back)
    return {
        "posts": posts,
        "meta": {
            "channels_processed": len(channel_list),
            "total_posts": len(posts)
        }
    }

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}