from telethon.tl.functions.messages import GetMessagesReactionsRequest

class EngagementProcessor:
    async def process(self, client, message, channel_entity):
        engagement = {
            "views": getattr(message, "views", 0),
            "forwards": getattr(message, "forwards", 0),
            "reactions": []
        }
        # Try direct reactions
        if hasattr(message, "reactions") and message.reactions:
            for reaction in message.reactions.results:
                engagement["reactions"].append({
                    "emoji": reaction.reaction.emoticon,
                    "count": reaction.count
                })
        else:
            # Try API request for reactions
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
                # Log or handle error if needed
                pass
        return engagement

async def get_reactions(client, channel_entity, message_id):
    try:
        response = await client(GetMessagesReactionsRequest(
            peer=channel_entity,
            id=[message_id]
        ))
        if hasattr(response, 'reactions'):
            for reaction in response.reactions:
                print(f"Emoji: {reaction.reaction}, Count: {reaction.count}")
        else:
            print("No reactions attribute in response")
    except Exception as e:
        print(f"Error: {e}")