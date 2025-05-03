class TextProcessor:
    def process(self, message):
        # Extract main text content, handle formatting, mentions, hashtags
        return getattr(message, "message", "")