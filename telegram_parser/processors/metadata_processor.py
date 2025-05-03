class MetadataProcessor:
    def process(self, message):
        # Example: extract has_link, link_domains
        has_link = False
        link_domains = []
        if hasattr(message, "entities") and message.entities:
            for entity in message.entities:
                if entity.__class__.__name__ == "MessageEntityUrl":
                    has_link = True
                    # Optionally extract domain from message text
        return {
            "has_link": has_link,
            "link_domains": link_domains
        }