from transformers import GPT2Tokenizer, GPT2LMHeadModel, set_seed
import time

start_time = time.time()
# Load the GPT-2 tokenizer and model
tokenizer: GPT2Tokenizer = GPT2Tokenizer.from_pretrained("gpt2-large")
set_seed(42)
# the head model adds a layer to the end of the standard GPT-large model that will predict the next tokens.
model: GPT2LMHeadModel = GPT2LMHeadModel.from_pretrained(
    "gpt2-large", pad_token_id=tokenizer.eos_token_id
)
end_time = time.time()

total_time = end_time - start_time
print("time to load:", total_time)

start_time = time.time()

# Generate some text
prompt = '"Yo Pete whats up!", john exclaimed. "Nothing much", pete replies. It was an quite night in london as the two discussed their dinner plans.'
input_ids = tokenizer.encode(prompt, return_tensors="pt")
outputs = model.generate(
    input_ids=input_ids,
    do_sample=True,
    max_length=200,
    top_p=0.92,
    top_k=20,
    num_return_sequences=1,
)
end_time = time.time()

total_time = end_time - start_time
print("time to generate:", total_time)


start_time = time.time()
for sequence in outputs:
    # Decode the generated text
    generated_text = tokenizer.decode(sequence, skip_special_tokens=True)

    # Print the generated text
    print(generated_text)
    print("---------------------------------------------")
end_time = time.time()

total_time = end_time - start_time
print("time to decode and print:", total_time)
