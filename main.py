"""
Telegram Channel Monitoring Service

This service monitors Telegram channels for posts and extracts data including:
- postId
- channelId
- postUrl
- postDate
- views
- reactions
- postType

It provides a REST API for n8n to query this data.
"""

import os
import json
import logging
import asyncio
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import uvicorn
from datetime import datetime, timezone
import sqlite3
from telethon import TelegramClient, utils
from telethon.tl.types import Channel, User, MessageMediaPhoto, MessageMediaDocument, MessageMediaPoll, MessageMediaWebPage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Environment variables for configuration
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE_NUMBER = os.getenv('TELEGRAM_PHONE')
SESSION_FILE = os.getenv('SESSION_FILE', 'telegram_session')
DB_PATH = os.getenv('DB_PATH', 'telegram_data.db')

# Initialize FastAPI
app = FastAPI(title="Telegram Channel Monitoring API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Database setup
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create channels table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS channels (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        title TEXT,
        last_updated TIMESTAMP
    )
    ''')
    
    # Create posts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        postId INTEGER,
        channelId INTEGER,
        postUrl TEXT,
        postDate TIMESTAMP,
        views INTEGER,
        reactions TEXT,  -- JSON string
        postType TEXT,
        content TEXT,
        PRIMARY KEY (postId, channelId),
        FOREIGN KEY (channelId) REFERENCES channels(id)
    )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Global client
client = None
client_lock = asyncio.Lock()

# Models
class ChannelInfo(BaseModel):
    username: str
    limit: Optional[int] = 50

class ChannelData(BaseModel):
    id: int
    username: str
    title: str
    last_updated: str

class Post(BaseModel):
    postId: int
    channelId: int
    postUrl: str
    postDate: str
    views: int
    reactions: Dict[str, int]
    postType: str
    content: Optional[str] = None

class PostsResponse(BaseModel):
    channel: ChannelData
    posts: List[Post]

# Helper to determine post type
def get_post_type(message):
    if message.media:
        if isinstance(message.media, MessageMediaPhoto):
            return "photo"
        elif isinstance(message.media, MessageMediaDocument):
            return "file"
        elif isinstance(message.media, MessageMediaPoll):
            return "poll"
        elif isinstance(message.media, MessageMediaWebPage):
            if message.media.webpage and message.media.webpage.type == "video":
                return "video"
    return "text"

# Helper to get post URL
def get_post_url(channel_username, message_id):
    return f"https://t.me/{channel_username}/{message_id}"

# Telethon client initialization
async def get_client():
    global client
    
    async with client_lock:
        if client is None or not client.is_connected():
            if not API_ID or not API_HASH:
                raise ValueError("TELEGRAM_API_ID and TELEGRAM_API_HASH environment variables must be set")
            
            logger.info("Initializing Telegram client")
            client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
            await client.start(phone=PHONE_NUMBER)
            
            # Save the session immediately
            client.session.save()
            
            logger.info("Telegram client connected")
    
    return client

# Schedule periodic updates
async def schedule_updates():
    while True:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM channels")
            channels = cursor.fetchall()
            conn.close()
            
            for channel in channels:
                await update_channel_data(channel[0])
            
            logger.info(f"Scheduled update completed for {len(channels)} channels")
        except Exception as e:
            logger.error(f"Error in scheduled update: {e}")
        
        # Wait for next update (every 30 minutes)
        await asyncio.sleep(30 * 60)

# Update data for a specific channel
async def update_channel_data(channel_username, limit=50):
    client = await get_client()
    
    try:
        # Get channel entity
        channel = await client.get_entity(channel_username)
        
        # Get channel ID
        channel_id = utils.get_peer_id(channel)
        
        # Get channel title
        channel_title = getattr(channel, 'title', channel_username)
        
        # Store channel info
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Insert or update channel
        cursor.execute(
            "INSERT OR REPLACE INTO channels (id, username, title, last_updated) VALUES (?, ?, ?, ?)",
            (channel_id, channel_username, channel_title, datetime.now(timezone.utc).isoformat())
        )
        
        # Get recent messages
        messages = await client.get_messages(channel, limit=limit)
        
        # Process and store messages
        for msg in messages:
            post_id = msg.id
            post_date = msg.date.isoformat() if msg.date else None
            post_url = get_post_url(channel_username, post_id)
            post_type = get_post_type(msg)
            content = msg.text or msg.message or None
            
            # Get reactions
            reactions = {}
            if hasattr(msg, 'reactions') and msg.reactions:
                for reaction in msg.reactions.results:
                    emoji = getattr(reaction.reaction, 'emoticon', str(reaction.reaction))
                    reactions[emoji] = reaction.count
            
            # Get views
            views = getattr(msg, 'views', 0)
            
            # Insert or update post
            cursor.execute(
                """
                INSERT OR REPLACE INTO posts 
                (postId, channelId, postUrl, postDate, views, reactions, postType, content) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (post_id, channel_id, post_url, post_date, views, json.dumps(reactions), post_type, content)
            )
        
        conn.commit()
        conn.close()
        
        logger.info(f"Updated data for channel {channel_username}, processed {len(messages)} messages")
        return True
    except Exception as e:
        logger.error(f"Error updating channel {channel_username}: {e}")
        return False

# API routes
@app.get("/")
def read_root():
    return {"message": "Telegram Channel Monitoring API", "status": "online"}

@app.get("/status")
async def get_status():
    try:
        client = await get_client()
        is_connected = client.is_connected()
        return {
            "status": "connected" if is_connected else "disconnected",
            "session_file": SESSION_FILE
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/channels")
async def add_channel(channel_info: ChannelInfo, background_tasks: BackgroundTasks):
    try:
        # Start the update in the background
        background_tasks.add_task(update_channel_data, channel_info.username, channel_info.limit)
        
        return {
            "message": f"Channel {channel_info.username} added for monitoring.",
            "status": "processing"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/channels")
async def list_channels():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, title, last_updated FROM channels")
    channels = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return {"channels": channels}

@app.get("/channels/{channel_username}")
async def get_channel_posts(channel_username: str, limit: int = 50):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get channel info
    cursor.execute("SELECT * FROM channels WHERE username = ?", (channel_username,))
    channel = cursor.fetchone()
    
    if not channel:
        # Try to get channel and update
        success = await update_channel_data(channel_username, limit)
        if not success:
            raise HTTPException(status_code=404, detail=f"Channel {channel_username} not found")
        
        # Get updated channel info
        cursor.execute("SELECT * FROM channels WHERE username = ?", (channel_username,))
        channel = cursor.fetchone()
    
    channel_dict = dict(channel)
    
    # Get posts for this channel
    cursor.execute(
        "SELECT * FROM posts WHERE channelId = ? ORDER BY postDate DESC LIMIT ?", 
        (channel_dict["id"], limit)
    )
    posts = cursor.fetchall()
    
    # Format posts
    formatted_posts = []
    for post in posts:
        post_dict = dict(post)
        post_dict["reactions"] = json.loads(post_dict["reactions"])
        formatted_posts.append(post_dict)
    
    conn.close()
    
    return {"channel": channel_dict, "posts": formatted_posts}

@app.get("/refresh/{channel_username}")
async def refresh_channel(channel_username: str, limit: int = 50):
    success = await update_channel_data(channel_username, limit)
    
    if not success:
        raise HTTPException(status_code=500, detail=f"Failed to update channel {channel_username}")
    
    return {"message": f"Channel {channel_username} updated successfully"}

@app.on_event("startup")
async def startup_event():
    try:
        # Initialize client
        await get_client()
        
        # Start background task for periodic updates
        asyncio.create_task(schedule_updates())
    except Exception as e:
        logger.error(f"Startup error: {e}")

# Run the API server
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)