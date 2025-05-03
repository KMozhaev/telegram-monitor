import logging
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetMessagesReactionsRequest
from .processors.text_processor import TextProcessor
from .processors.media_processor import MediaProcessor
from .processors.engagement_processor import EngagementProcessor
from .processors.metadata_processor import MetadataProcessor

class TelegramParser:
    def __init__(self, api_id, api_hash, phone):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.logger = logging.getLogger(__name__)
        self.text_processor = TextProcessor()
        self.media_processor = MediaProcessor()
        self.engagement_processor = EngagementProcessor()
        self.metadata_processor = MetadataProcessor()

    async def get_posts(self, channel_list, limit=10, days_back=None):
        client = TelegramClient('parser_session', self.api_id, self.api_hash)
        await client.start(phone=self.phone)
        results = []
        for channel in channel_list:
            try:
                channel_entity = await client.get_entity(channel)
                channel_info = await client(GetFullChannelRequest(channel=channel_entity))
                date_filter = None
                if days_back:
                    date_filter = datetime.now() - timedelta(days=days_back)
                messages = await client.get_messages(channel_entity, limit=limit)
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
                        "engagement": await self.engagement_processor.process(client, channel_entity, msg),
                        **self.metadata_processor.process(msg)
                    }
                    results.append(processed_post)
            except Exception as e:
                self.logger.error(f"Error processing channel {channel}: {str(e)}")
        await client.disconnect()
        return results

async def fetch_reactions(client, channel_entity, message_id):
    try:
        response = await client(GetMessagesReactionsRequest(
            peer=channel_entity,
            id=[message_id]
        ))
        # The response should have a .reactions attribute (a list)
        reactions = []
        if hasattr(response, 'reactions'):
            for reaction in response.reactions:
                # reaction.reaction can be an object or a string
                emoji = getattr(reaction.reaction, "emoticon", None) or getattr(reaction.reaction, "document_id", None) or reaction.reaction
                reactions.append({
                    "emoji": emoji,
                    "count": reaction.count
                })
        return reactions
    except Exception as e:
        print(f"Error fetching reactions: {e}")
        return []

class EngagementProcessor:
    async def process(self, client, channel_entity, message):
        engagement = {
            "views": getattr(message, "views", 0),
            "forwards": getattr(message, "forwards", 0),
            "reactions": []
        }
        # Try to get reactions directly
        if hasattr(message, "reactions") and message.reactions:
            for reaction in message.reactions.results:
                engagement["reactions"].append({
                    "emoji": getattr(reaction.reaction, "emoticon", None),
                    "count": reaction.count
                })
        else:
            # Fallback: use GetMessagesReactionsRequest
            try:
                reactions_response = await client(GetMessagesReactionsRequest(
                    peer=channel_entity,
                    id=[message.id]
                ))
                if hasattr(reactions_response, "reactions"):
                    for reaction in reactions_response.reactions:
                        engagement["reactions"].append({
                            "emoji": getattr(reaction.reaction, "emoticon", None),
                            "count": reaction.count
                        })
            except Exception as e:
                # Optionally log the error
                pass
        return engagement