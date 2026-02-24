import json
from pathlib import Path

from data_process import load_reviews
from engine import Engine

engine = Engine(device="metal", model_choice=Engine.model_choice.ministral_3b)

reviews = load_reviews(Path("./PGraphRAG/amazon_train.json"))

for idx, review in enumerate(reviews, 1):
    print(f"\n--- Review {idx}/{len(reviews)} ---")
    print(f"Product: {review['product_id']} | Rating: {review['rating']}")
    print(f"Text: {review['text']}")

    response = engine.send_extract_message(f"Text: {review['text']}")
    output = response.choices[0].message.content

    try:
        parsed_json = json.loads(output)
        with open("./PGraphRAG/output/amazon_train_output.jsonl", "a") as f:
            f.write(json.dumps(parsed_json) + "\n")
    except json.JSONDecodeError:
        print(f"Warning: Model output for review {idx} was not valid JSON.")

    print(f"Triples:\n{output}")

engine.terminate()