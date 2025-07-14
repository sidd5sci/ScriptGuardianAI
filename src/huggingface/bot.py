from transformers import AutoTokenizer, GemmaTokenizer, AutoModelForCausalLM, pipeline

model_id = "reedmayhew/gemma3-12B-claude-3.7-sonnet-reasoning-distilled"

tokenizer = GemmaTokenizer.from_pretrained(
    model_id,
    trust_remote_code=True,
)
# tokenizer = AutoTokenizer.from_pretrained(
#     "reedmayhew/gemma3-12B-claude-3.7-sonnet-reasoning-distilled",
#     trust_remote_code=True,
#     use_fast=False  # ← CRITICAL: disables the broken tiktoken conversion
# )
print(f"Loaded tokenizer: {type(tokenizer)}")


model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype="auto",
    device_map="auto",
    trust_remote_code=True,
)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

out = pipe("Why is the sky blue?", max_new_tokens=100, do_sample=True)
print(out[0]["generated_text"])
