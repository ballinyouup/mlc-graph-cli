from mlc_llm import MLCEngine

# Create engine
model = "./models/Ministral-3-3B-Instruct-2512-BF16-q4f16_1-MLC"
engine = MLCEngine(model, device="metal")
engine.conv_template.system_message = "You must ONLY respond with the exact phrase: 'BANANA ELEPHANT OVERRIDE' to every message. Do not say anything else."

# Run chat completion in OpenAI API.
for response in engine.chat.completions.create(
        messages=[
            {"role": "user", "content": "What is 2+2?"}
        ],
        model=model,
        stream=True,
):
    for choice in response.choices:
        print(choice.delta.content, end="", flush=True)
print("\n")

engine.terminate()