import logging
import time
import random
import asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.errors import FloodWaitError
from .processors.text_processor import TextProcessor
from .processors.media_processor import MediaProcessor
from .processors.engagement_processor import EngagementProcessor
from .processors.metadata_processor import MetadataProcessor

class TelegramParser:
    def __init__(self, api_id, api_hash, phone, session_string=None, session_file='parser_session'):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.session_string = session_string
        self.session_file = session_file
        self.logger = logging.getLogger(__name__)
        
        # Initialize processors
        self.text_processor = TextProcessor()
        self.media_processor = MediaProcessor()
        self.engagement_processor = EngagementProcessor()
        self.metadata_processor = MetadataProcessor()
        
        # Rate limiting properties
        self.request_count = 0
        self.last_request_time = 0
        self.max_requests_per_minute = 20  # Conservative limit

    async def _rate_limit(self):
        """Implement rate limiting to avoid blocks"""
        current_time = time.time()
        time_passed = current_time - self.last_request_time
        
        # If we've made too many requests in the past minute, sleep
        if self.request_count >= self.max_requests_per_minute and time_passed < 60:
            sleep_time = 60 - time_passed + random.uniform(1, 5)  # Add jitter
            self.logger.info(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            await asyncio.sleep(sleep_time)
            self.request_count = 0
            self.last_request_time = time.time()
        
        # If more than a minute has passed, reset counter
        elif time_passed >= 60:
            self.request_count = 0
            self.last_request_time = current_time
        
        # Increment request counter
        self.request_count += 1

    async def get_posts(self, channel_list, limit=10, days_back=None):
        """Get posts from specified channels with rate limiting and anti-block measures"""
        # Initialize client with string session if available, otherwise use file session
        if self.session_string:
            client = TelegramClient(StringSession(self.session_string), self.api_id, self.api_hash)
            self.logger.info("Using StringSession for authentication")
        else:
            client = TelegramClient(self.session_file, self.api_id, self.api_hash)
            self.logger.info("Using file-based session for authentication")
        
        try:
            # Connect to client
            await client.connect()
            
            # Check authorization
            if not await client.is_user_authorized():
                if self.session_string:
                    self.logger.error("StringSession is not valid or expired")
                    raise Exception("StringSession authentication failed")
                elif not self.phone:
                    self.logger.error("No phone number provided for authentication")
                    raise Exception("Authentication required but no phone number provided")
                else:
                    self.logger.info("First-time authentication required")
                    # This will cause problems in non-interactive environments
                    # Only used for local development
                    await client.send_code_request(self.phone)
                    code = input('Enter the code you received: ')
                    await client.sign_in(self.phone, code)
                
            results = []
            
            for channel in channel_list:
                try:
                    # Apply rate limiting before each request
                    await self._rate_limit()
                    
                    # Add random delay between channels to appear more human-like
                    await asyncio.sleep(random.uniform(2, 5))
                    
                    # Get channel entity
                    channel_entity = await client.get_entity(channel)
                    
                    # Add small delay before next API call
                    await asyncio.sleep(random.uniform(1, 2))
                    
                    # Apply rate limiting again
                    await self._rate_limit()
                    
                    # Get channel info
                    channel_info = await client(GetFullChannelRequest(channel=channel_entity))
                    
                    # Calculate date filter if days_back specified
                    date_filter = None
                    if days_back:
                        date_filter = datetime.now() - timedelta(days=days_back)
                    
                    # Apply rate limiting before getting messages
                    await self._rate_limit()
                    
                    # Get messages (with retry logic)
                    try:
                        messages = await client.get_messages(
                            channel_entity, 
                            limit=limit
                        )
                        
                        for msg in messages:
                            # Skip messages older than date_filter if specified
                            if date_filter and msg.date.replace(tzinfo=None) < date_filter:
                                continue
                            
                            # Process message with MCPs
                            processed_post = {
                                "channel_username": channel,
                                "channel_title": getattr(channel_entity, "title", ""),
                                "post_id": msg.id,
                                "date": msg.date.isoformat(),
                                "text": self.text_processor.process(msg),
                                "media": self.media_processor.process(msg),
                                "engagement": await self.engagement_processor.process(client, msg, channel_entity),
                                **self.metadata_processor.process(msg)
                            }
                            
                            results.append(processed_post)
                            
                            # Add small delay between processing messages
                            await asyncio.sleep(random.uniform(0.3, 0.7))
                            
                    except FloodWaitError as e:
                        wait_time = e.seconds
                        self.logger.error(f"Rate limit hit for {channel}. Need to wait {wait_time} seconds.")
                        if wait_time < 300:  # Only retry for short waits
                            self.logger.info(f"Waiting {wait_time} seconds before retry...")
                            await asyncio.sleep(wait_time + 10)  # Add buffer time
                            # Get messages with reduced limit
                            retry_limit = max(1, limit//2)
                            self.logger.info(f"Retrying with reduced limit of {retry_limit}")
                            
                            # Apply rate limiting again
                            await self._rate_limit()
                            
                            messages = await client.get_messages(
                                channel_entity, 
                                limit=retry_limit
                            )
                            
                            for msg in messages:
                                if date_filter and msg.date.replace(tzinfo=None) < date_filter:
                                    continue
                                
                                processed_post = {
                                    "channel_username": channel,
                                    "channel_title": getattr(channel_entity, "title", ""),
                                    "post_id": msg.id,
                                    "date": msg.date.isoformat(),
                                    "text": self.text_processor.process(msg),
                                    "media": self.media_processor.process(msg),
                                    "engagement": await self.engagement_processor.process(client, msg, channel_entity),
                                    **self.metadata_processor.process(msg)
                                }
                                
                                results.append(processed_post)
                                
                                # Add small delay between processing messages
                                await asyncio.sleep(random.uniform(0.3, 0.7))
                        else:
                            self.logger.error(f"Wait time too long ({wait_time}s) for {channel}. Skipping.")
                    
                except Exception as e:
                    self.logger.error(f"Error processing channel {channel}: {str(e)}")
                    # Continue with next channel instead of failing completely
                    continue
            
            self.logger.info(f"Successfully processed {len(results)} posts from {len(channel_list)} channels")
            return results
            
        except Exception as e:
            self.logger.error(f"Error in get_posts: {str(e)}")
            raise
            
        finally:
            # Always disconnect client
            await client.disconnect()
            self.logger.info("Client disconnected")