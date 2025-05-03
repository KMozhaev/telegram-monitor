import os
import logging
import json
from dotenv import load_dotenv
from telethon import TelegramClient, events
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetMessagesReactionsRequest

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE')

# List of channels to monitor (add channel usernames)
CHANNELS_TO_MONITOR = [
    'meduzionok',
    'vcnews'
]

async def main():
    logger.info("Starting Telegram monitor")
    
    # Create the client and connect
    client = TelegramClient('monitor_session', API_ID, API_HASH)
    await client.start(phone=PHONE)
    
    logger.info("Connected to Telegram!")
    
    # Verify the channels exist and we can access them
    for channel in CHANNELS_TO_MONITOR:
        try:
            channel_entity = await client.get_entity(channel)
            channel_full = await client(GetFullChannelRequest(channel=channel_entity))
            
            logger.info(f"Successfully connected to channel: {channel}")
            logger.info(f"Channel info: {channel_entity.title} | {channel_full.full_chat.about}")
            
            # Get the 5 most recent messages
            messages = await client.get_messages(channel_entity, limit=5)
            logger.info(f"Retrieved {len(messages)} messages from {channel}")
            
            for msg in messages:
                logger.info(f"Message ID: {msg.id} | Date: {msg.date} | Text: {msg.text[:100]}...")
                
                # Check for views
                if hasattr(msg, 'views'):
                    logger.info(f"Views for message {msg.id}: {msg.views}")
                else:
                    logger.info(f"No views data found for message {msg.id}")
                    
                # Check for forwards
                if hasattr(msg, 'forwards'):
                    logger.info(f"Forwards for message {msg.id}: {msg.forwards}")
                else:
                    logger.info(f"No forwards data found for message {msg.id}")
                
                # Direct inspection of the message object for reactions
                if hasattr(msg, 'reactions'):
                    logger.info(f"Reactions found directly on message object for {msg.id}:")
                    logger.info(f"Reactions data: {msg.reactions}")
                
                # Examine all available attributes for reaction-related data
                logger.info(f"Available message attributes for {msg.id}:")
                for attr in dir(msg):
                    if not attr.startswith('_') and not callable(getattr(msg, attr)):
                        try:
                            attr_value = getattr(msg, attr)
                            if attr_value is not None and attr not in ['text', 'message', 'raw_text']:
                                logger.info(f"  - {attr}: {attr_value}")
                        except Exception as e:
                            pass
                
                # Try the GetMessagesReactionsRequest approach as well
                try:
                    reactions_response = await client(GetMessagesReactionsRequest(
                        peer=channel_entity,
                        id=[msg.id]
                    ))
                    
                    logger.info(f"GetMessagesReactionsRequest response type: {type(reactions_response)}")
                    logger.info(f"GetMessagesReactionsRequest attributes: {dir(reactions_response)}")
                    
                    # Check if the response has reactions attribute
                    if hasattr(reactions_response, 'reactions'):
                        logger.info(f"Reactions for message {msg.id} from API request:")
                        for reaction in reactions_response.reactions:
                            logger.info(f"  - Reaction: {reaction.reaction} | Count: {reaction.count}")
                    else:
                        logger.info(f"No reactions attribute in API response for message {msg.id}")
                        
                except Exception as e:
                    logger.error(f"Error getting reactions for message {msg.id}: {e}")
                    
        except Exception as e:
            logger.error(f"Error accessing channel {channel}: {e}")
    
    # Disconnect the client
    await client.disconnect()
    logger.info("Disconnected from Telegram")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())