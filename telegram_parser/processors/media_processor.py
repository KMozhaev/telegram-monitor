from telethon.tl.functions.messages import GetMessagesReactionsRequest

async def get_reactions(client, channel_entity, message):
    reactions = []
    # 1. Try direct attribute
    if hasattr(message, "reactions") and message.reactions and hasattr(message.reactions, "results"):
        for reaction in message.reactions.results:
            reactions.append({
                "emoji": getattr(reaction.reaction, "emoticon", None),
                "count": reaction.count
            })
    else:
        # 2. Fallback: explicit API call
        try:
            resp = await client(GetMessagesReactionsRequest(
                peer=channel_entity,
                id=[message.id]
            ))
            if hasattr(resp, "reactions"):
                for reaction in resp.reactions:
                    reactions.append({
                        "emoji": getattr(reaction.reaction, "emoticon", None),
                        "count": reaction.count
                    })
        except Exception as e:
            # Optionally log the error
            pass
    return reactions

class MediaProcessor:
    def process(self, message):
        return []