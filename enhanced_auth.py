#!/usr/bin/env python
"""
Enhanced Telegram Authentication Script

This script authenticates with Telegram, joins specified channels,
and verifies access before saving the session file.
"""

import asyncio
import os
import sys
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors import (
    AuthKeyUnregisteredError,
    ChannelPrivateError,
    InviteRequestSentError,
    UsernameNotOccupiedError,
)
from telethon import utils

# Get environment variables or use defaults
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE = os.getenv('TELEGRAM_PHONE')
SESSION_FILE = os.getenv('SESSION_FILE', 'telegram_session')
PERSIST_PATH = os.getenv('DB_PATH', '/app/data').split('/telegram_data.db')[0]

# List of channels to monitor
TARGET_CHANNELS = [
    'durov',                 # Try without @
    '@durov',                # Try with @
    'telegram',              # Another official channel
    'tjournalru',            # Alternative channel to test
    'techcrunch',            # News channel, generally accessible
]

async def main():
    print("-" * 50)
    print("Telegram Enhanced Authentication Script")
    print("-" * 50)
    print(f"API ID: {API_ID}")
    print(f"Phone: {PHONE}")
    print(f"Session File: {SESSION_FILE}")
    print(f"Persistence Path: {PERSIST_PATH}")
    print("-" * 50)
    
    # Create client but don't start it yet
    client = TelegramClient(SESSION_FILE, API_ID, API_HASH)
    
    try:
        # Start the client and authenticate
        print("Starting client and authenticating...")
        await client.start(phone=PHONE)
        
        # Verify authentication
        if not await client.is_user_authorized():
            print("❌ Authentication failed! Please check your credentials.")
            return False
        
        print("✅ Successfully authenticated!")
        
        # Get self info to confirm we're properly connected
        me = await client.get_me()
        print(f"Logged in as: {me.first_name} {me.last_name} (@{me.username})")
        
        # Try to join and access each channel
        successful_channels = []
        failed_channels = []
        
        for channel_name in TARGET_CHANNELS:
            try:
                print(f"\nTrying to access channel: {channel_name}")
                
                # First try to get the channel entity
                try:
                    channel = await client.get_entity(channel_name)
                    channel_id = utils.get_peer_id(channel)
                    print(f"✅ Successfully retrieved channel entity: {channel.title} (ID: {channel_id})")
                except UsernameNotOccupiedError:
                    print(f"❌ Channel {channel_name} does not exist!")
                    failed_channels.append((channel_name, "does_not_exist"))
                    continue
                except ValueError as e:
                    print(f"❌ Error getting channel entity: {e}")
                    failed_channels.append((channel_name, "entity_error"))
                    continue
                
                # Try to join the channel (if needed)
                try:
                    print(f"Attempting to join channel {channel_name}...")
                    await client(JoinChannelRequest(channel))
                    print(f"✅ Successfully joined channel {channel_name}")
                except TypeError:
                    # This often happens when already joined
                    print(f"ℹ️ May already be a member of {channel_name}")
                except ChannelPrivateError:
                    print(f"❌ Cannot join private channel {channel_name}")
                    failed_channels.append((channel_name, "private_channel"))
                    continue
                except InviteRequestSentError:
                    print(f"ℹ️ Join request sent to {channel_name}, waiting for approval")
                    failed_channels.append((channel_name, "join_request_sent"))
                    continue
                except Exception as e:
                    print(f"ℹ️ Join info: {e}")
                
                # Test getting messages
                try:
                    messages = await client.get_messages(channel, limit=1)
                    if messages and len(messages) > 0:
                        print(f"✅ Successfully retrieved messages from {channel_name}")
                        successful_channels.append(channel_name)
                    else:
                        print(f"⚠️ No messages found in {channel_name}")
                        successful_channels.append(channel_name)  # Still count as success since we could access it
                except Exception as e:
                    print(f"❌ Error getting messages: {e}")
                    failed_channels.append((channel_name, f"message_error: {str(e)}"))
            
            except Exception as e:
                print(f"❌ Unexpected error with channel {channel_name}: {e}")
                failed_channels.append((channel_name, f"unexpected: {str(e)}"))
                
        # Summarize results
        print("\n" + "=" * 50)
        print("CHANNEL ACCESS SUMMARY")
        print("=" * 50)
        
        print(f"\n✅ Successfully accessed {len(successful_channels)} channels:")
        for channel in successful_channels:
            print(f"  - {channel}")
            
        print(f"\n❌ Failed to access {len(failed_channels)} channels:")
        for channel, reason in failed_channels:
            print(f"  - {channel} (Reason: {reason})")
        
        # Save session to persistent storage
        session_file = f"{SESSION_FILE}.session"
        target_path = os.path.join(PERSIST_PATH, session_file)
        
        if os.path.exists(session_file):
            print(f"\nSaving session file to {target_path}")
            # Create directory if it doesn't exist
            os.makedirs(PERSIST_PATH, exist_ok=True)
            # Copy the session file
            import shutil
            shutil.copy(session_file, target_path)
            print(f"✅ Session file saved to {target_path}")
        else:
            print(f"❌ Session file {session_file} not found!")
            
        return len(successful_channels) > 0
        
    except AuthKeyUnregisteredError:
        print("❌ Authentication key not registered. You need to re-authenticate.")
        return False
    except Exception as e:
        print(f"❌ Error during authentication process: {e}")
        return False
    finally:
        print("\nDisconnecting client...")
        await client.disconnect()
        print("Done!")

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)