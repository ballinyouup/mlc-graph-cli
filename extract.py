import asyncio
import json
from pathlib import Path

def load_completed_indices(output_path):
    completed = set()
    path = Path(output_path)
    if path.exists():
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    if "idx" in record:
                        completed.add(record["idx"])
                except json.JSONDecodeError:
                    continue
    return completed

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
    print(f"Loaded {len(reviews)} reviews from {path}")
    return reviews

async def process_review(idx, review, engine, pbar, output_path, semaphore, write_lock):
    async with semaphore:
        print(f"\n--- Review {idx} ---")
        print(f"Product: {review['product_id']} | Rating: {review['rating']}")
        print(f"Text: {review['text']}")

        max_retries = 10
        for attempt in range(max_retries):
            try:
                response = await engine.send_extract_message(f"Text: {review['text']}")
                output = response.choices[0].message.content

                parsed_json = json.loads(output)
                
                # Handle case where the model returns a list instead of dict
                if isinstance(parsed_json, list):
                    print(f"Warning: Model returned list instead of dict on attempt {attempt + 1}. Retrying...")
                    continue
                
                # Handle case where the model returns the dict without a "triples" key
                if "triples" not in parsed_json:
                    print(f"Warning: Model output missing 'triples' key on attempt {attempt + 1}. Retrying...")
                    continue
                
                # Success - add metadata and write
                parsed_json["idx"] = idx
                parsed_json["user_id"] = review["user_id"]
                parsed_json["product_id"] = review["product_id"]
                async with write_lock:
                    with open(output_path, "a") as f:
                        f.write(json.dumps(parsed_json) + "\n")
                        f.flush()
                
                print(f"Triples:\n{output}")
                break
                
            except json.JSONDecodeError as e:
                print(f"Warning: Model output was not valid JSON on attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    print(f"Failed to get valid output for review {idx} after {max_retries} attempts.")
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"Warning: Error on attempt {attempt + 1}: {type(e).__name__}: {e}")
                if attempt == max_retries - 1:
                    print(f"Failed to process review {idx} after {max_retries} attempts.")
                await asyncio.sleep(0.5)

        pbar.update(1)
