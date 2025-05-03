import asyncio
import os
import logging
from flask import Flask, request, jsonify
from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE')

app = Flask(__name__)

# Global client variable
client = None

def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()
        raise

async def get_client():
    global client
    if client is None or not client.is_connected():
        client = TelegramClient('monitor_session', API_ID, API_HASH)
        await client.start(phone=PHONE)
    return client

async def get_channel_posts(channel_username, limit=10):
    client = await get_client()
    
    try:
        channel_entity = await client.get_entity(channel_username)
        messages = await client.get_messages(channel_entity, limit=limit)
        
        result = []
        for msg in messages:
            post_data = {
                "id": msg.id,
                "date": msg.date.isoformat(),
                "text": msg.text if msg.text else "",
                "views": getattr(msg, 'views', 0),
                "forwards": getattr(msg, 'forwards', 0),
            }
            
            if hasattr(msg, 'media') and msg.media:
                post_data["has_media"] = True
                post_data["media_type"] = type(msg.media).__name__
            else:
                post_data["has_media"] = False
            
            result.append(post_data)
        
        return result
    
    except Exception as e:
        logger.error(f"Error fetching posts from {channel_username}: {e}")
        return {"error": str(e)}

@app.route('/api/fetch-posts', methods=['POST'])
def fetch_posts():
    data = request.json
    
    if not data or 'channels' not in data:
        return jsonify({"error": "Invalid request, 'channels' field is required"}), 400
    
    channels = data['channels']
    limit = data.get('limit', 10)
    
    # Setup event loop for async operations
    loop = get_or_create_eventloop()
    
    results = {}
    for channel in channels:
        channel_posts = loop.run_until_complete(get_channel_posts(channel, limit))
        results[channel] = channel_posts
    
    return jsonify(results)

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"})

if __name__ == '__main__':
    print("Starting Flask API...")
    app.run(host='0.0.0.0', port=5000, debug=True)