"""
Message Content Processors (MCPs) for Telegram posts
These processors normalize and filter the post data before output
"""

def clean_text(text):
    """Clean and normalize post text"""
    if not text:
        return ""
    # Replace multiple newlines with single newline
    import re
    text = re.sub(r'\n+', '\n', text)
    # Trim whitespace
    return text.strip()

def extract_hashtags(text):
    """Extract hashtags from post text"""
    if not text:
        return []
    import re
    hashtags = re.findall(r'#(\w+)', text)
    return hashtags

def extract_urls(text):
    """Extract URLs from post text"""
    if not text:
        return []
    import re
    urls = re.findall(r'https?://\S+', text)
    return urls

def process_post(post_data):
    """Apply all processors to a post"""
    if not post_data:
        return post_data
        
    # Apply text processors
    if 'text' in post_data:
        post_data['text'] = clean_text(post_data['text'])
        post_data['hashtags'] = extract_hashtags(post_data['text'])
        post_data['urls'] = extract_urls(post_data['text'])
    
    # Calculate engagement metrics
    reactions_count = sum(r['count'] for r in post_data.get('reactions', []))
    post_data['engagement'] = {
        'views': post_data.get('views', 0),
        'forwards': post_data.get('forwards', 0),
        'reactions': reactions_count,
        'total': post_data.get('views', 0) + post_data.get('forwards', 0) + reactions_count
    }
    
    return post_data

def process_channel_posts(posts):
    """Process a list of posts from a channel"""
    return [process_post(post) for post in posts]