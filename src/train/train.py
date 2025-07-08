from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import prepare_model_for_kbit_training, LoraConfig, get_peft_model
from datasets import load_dataset
import torch

model_name = "mistralai/Mistral-7B-v0.1"

tokenizer = AutoTokenizer.from_pretrained(model_name, token="hf_xxxxx", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    load_in_4bit=True,
    device_map="auto",
    trust_remote_code=True
)

model = prepare_model_for_kbit_training(model)

peft_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, peft_config)

# Load your dataset
dataset = load_dataset("json", data_files="dataset.jsonl", split="train")

# Tokenization
def tokenize(example):
    messages = example["messages"]
    prompt = "".join([f"<|{m['role']}|>\n{m['content']}\n" for m in messages])
    tokens = tokenizer(prompt, truncation=True, padding="max_length", max_length=2048)
    tokens["labels"] = tokens["input_ids"].copy()
    return tokens

tokenized = dataset.map(tokenize, remove_columns=["messages"])

# Training setup
training_args = TrainingArguments(
    output_dir="./mistral-scanbee-lora",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    logging_steps=10,
    num_train_epochs=3,
    save_strategy="epoch",
    learning_rate=2e-5,
    bf16=torch.cuda.is_bf16_supported(),
    fp16=not torch.cuda.is_bf16_supported(),
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized,
    tokenizer=tokenizer
)

trainer.train()
