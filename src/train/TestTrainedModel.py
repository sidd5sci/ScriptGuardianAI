from transformers import pipeline
from peft import PeftModel
base = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1", device_map="auto", load_in_4bit=True)
model = PeftModel.from_pretrained(base, "./mistral")
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
