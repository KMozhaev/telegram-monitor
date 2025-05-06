import asyncio
import random
from telethon.tl.functions.messages import GetMessagesReactionsRequest

class EngagementProcessor:
    async def process(self, client, message, channel_entity):
        """Extract engagement metrics from a message with anti-blocking measures"""
        engagement = {
            "views": getattr(message, "views", 0),
            "forwards": getattr(message, "forwards", 0),
            "reactions": []
        }
        
        # Try direct reactions first (less API intensive)
        if hasattr(message, "reactions") and message.reactions:
            for reaction in message.reactions.results:
                engagement["reactions"].append({
                    "emoji": getattr(reaction.reaction, "emoticon", None),
                    "count": reaction.count
                })
            return engagement
        
        # Only make additional API request if necessary and with delay
        try:
            # Add random delay before API call to appear more natural
            await asyncio.sleep(random.uniform(0.5, 1.5))
            
            reactions_response = await client(GetMessagesReactionsRequest(
                peer=channel_entity,
                id=[message.id]
            ))
            
            if hasattr(reactions_response, "reactions"):
                for reaction in reactions_response.reactions:
                    engagement["reactions"].append({
                        "emoji": getattr(reaction.reaction, "emoticon", None) or str(reaction.reaction),
                        "count": reaction.count
                    })
        except Exception as e:
            # Just log and continue - reactions are optional
            pass
            
        return engagement