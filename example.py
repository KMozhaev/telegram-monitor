from datetime import datetime, timedelta, timezone

async def fetch_posts(client, channels, limit=10, days_back=None):
    posts = []
    cutoff = None
    if days_back is not None:
        from datetime import timezone
        cutoff = datetime.now(timezone.utc) - timedelta(days=days_back)

    for chan in channels:
        count = 0
        async for msg in client.iter_messages(chan, limit=limit):
            count += 1
            print(f"[DEBUG] got msg id={msg.id} date={msg.date} from {chan}")
            if cutoff and msg.date < cutoff:
                print(f"[DEBUG]   → skipping {msg.id}, older than cutoff")
                continue

            posts.append({
                'channel': chan,
                'id': msg.id,
                'date': msg.date.isoformat(),
                'text': msg.text or '',
                'media': [],    # упростили для теста
                'views': getattr(msg, 'views', None),
                'reactions': getattr(msg, 'reactions', None),
                'forwards': getattr(msg, 'forwards', None),
            })
        print(f"[DEBUG] iterated {count} messages in {chan}")
    return posts
