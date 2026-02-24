import json
def load_reviews(path):
    reviews = []
    with open(path, 'r') as f:
        data = json.load(f)
        for user in data:
            for review in user.get("profile", []):
                reviews.append({
                    "user_id": user["id"],
                        "product_id": review["pid"],
                        "rating": review["rating"],
                        "title": review["title"],
                        "text": review["text"]
                    })
    print(f"Loaded {len(reviews)} reviews from {len(list(path.glob('*.json')))} files")
    return reviews