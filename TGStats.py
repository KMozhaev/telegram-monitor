import requests

TOKEN   = "44ed30c7070d580678a4b2b6ef6b4044"
POST_ID = "https://t.me/productsmemes/1097"

resp = requests.get(
    "https://api.tgstat.ru/posts/stat",
    params={"token": TOKEN, "postId": POST_ID}
)
data = resp.json()

if data.get("status") == "ok":
    stats = data["response"]
    print("Просмотров:",     stats["viewsCount"])
    print("Реакций:",        stats["reactionsCount"])
    print("Пересылок:",      stats["sharesCount"])
    print("Репостов в каналы:", stats["forwardsCount"])
else:
    print("Ошибка:", data)
