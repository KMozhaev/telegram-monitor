from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os
from dotenv import load_dotenv

# Load values from .env file
load_dotenv()

# Get API credentials from environment or enter manually
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE')

# Prompt for values if not found in environment
if not API_ID or API_ID == 'API_ID':
    API_ID = input("Enter your API ID: ")
    
if not API_HASH or API_HASH == 'API_HASH':
    API_HASH = input("Enter your API HASH: ")
    
if not PHONE or PHONE == 'PHONE':
    PHONE = input("Enter your phone number (with country code): ")

# Convert API_ID to integer
API_ID = int(API_ID)

# Create session and connect
with TelegramClient(StringSession(), API_ID, API_HASH) as client:
    print("Connecting to Telegram...")
    client.start(phone=PHONE)
    
    # Get the session string
    session_string = client.session.save()
    
    print("\n\n===== SAVE THIS STRING SESSION (do not share it) =====")
    print(session_string)
    print("=======================================================\n\n")
    
    print("Authentication successful!")
    print("You can now add this string to your environment variables as SESSION_STRING")