import os
from dotenv import load_dotenv
from telethon import TelegramClient
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Telegram API credentials
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE')

async def get_channel_posts(channel_username, limit=10):
    """
    Basic function to fetch posts from a Telegram channel
    
    Args:
        channel_username (str): Username of the channel (without @)
        limit (int): Maximum number of posts to fetch
        
    Returns:
        list: List of post data dictionaries
    """
    # Create client
    client = TelegramClient('session_name', API_ID, API_HASH)
    
    # Start client
    await client.start(phone=PHONE)
    print(f"Client started successfully")
    
    try:
        # Get channel entity
        channel = await client.get_entity(channel_username)
        print(f"Found channel: {channel.title}")
        
        # Get messages
        messages = await client.get_messages(channel, limit=limit)
        print(f"Retrieved {len(messages)} messages")
        
        # Process messages
        results = []
        for msg in messages:
            # Extract reactions data if available
            reactions = []
            if hasattr(msg, 'reactions') and msg.reactions:
                for reaction in msg.reactions.results:
                    reactions.append({
                        'emoji': reaction.reaction.emoticon,
                        'count': reaction.count
                    })
            
            # Process media information
            media_info = None
            if msg.media:
                media_type = msg.media.__class__.__name__
                media_info = {
                    'type': media_type
                }
                
            post_data = {
                'id': msg.id,
                'date': msg.date.isoformat(),
                'text': msg.text,
                'views': getattr(msg, 'views', 0),
                'forwards': getattr(msg, 'forwards', 0),
                'replies': getattr(msg, 'replies', 0),
                'reactions': reactions,
                'media': media_info
            }
            
            results.append(post_data)
            
        return results
            
    except Exception as e:
        print(f"Error: {e}")
        return []
    
    finally:
        # Disconnect the client
        await client.disconnect()
        print("Client disconnected")

# Test script
if __name__ == "__main__":
    import asyncio
    
    async def main():
        # Example channel (replace with a public channel)
        channel_name = "durov"  # Pavel Durov's channel
        
        posts = await get_channel_posts(channel_name, limit=5)
        
        # Print results
        for post in posts:
            print(f"\nPost ID: {post['id']}")
            print(f"Date: {post['date']}")
            print(f"Views: {post['views']}")
            print(f"Forwards: {post['forwards']}")
            print(f"Replies: {post['replies']}")
            print(f"Text: {post['text'][:100]}..." if len(post['text']) > 100 else f"Text: {post['text']}")
            print(f"Media: {post['media']}")
            
            # Print reactions if any
            if post['reactions']:
                print("Reactions:")
                for reaction in post['reactions']:
                    print(f"  {reaction['emoji']}: {reaction['count']}")
            else:
                print("Reactions: None")
    
    asyncio.run(main())