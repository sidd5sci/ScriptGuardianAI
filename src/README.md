# ScriptGuardian

Security‑issue detector for PowerShell & Groovy scripts.  
Uses a *local* LLM (Mistral, Claude Sonnet via Ollama.) plus a **vector store** of labelled examples for k‑shot RAG.

## Quick start

```bash
git clone <repo>
cd ScriptGuardian

brew update
brew install pyenv
brew install pyenv-virtualenv

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
# Load pyenv-virtualenv into the shell
eval "$(pyenv virtualenv-init -)"


pyenv install 3.10.13
pyenv virtualenv 3.10.13 env

source ~/.zshrc
pyenv activate env

pip3 install -r requirements.txt
```

other way 
```sh
python -m venv .venv && source .venv/bin/activate
pip install -e .
```
## start ollama if using 
```bash
ollama pull nomic-embed-text
ollama pull codellama:latest
ollama pull llama3:latest
ollama serve
```
## Start LM studio if using


# 1. Build the vector DB from your labelled corpus


# 2. Scan scripts


# 3. Evaluate


```sh
pip3 install pandas
pip3 install transformers
pip3 install peft
pip3 install datasets
pip3 install langchain
pip3 install langchain_community
pip3 install sentence-transformers
pip3 install chromadb
pip3 install bitsandbytes
pip3 install -U langchain-ollama
pip install datasets sentence-transformers requests
pip3 install --upgrade cffi
pip install transformers peft datasets bitsandbytes accelerate


pip3 install requests beautifulsoup4

pip3 install fastapi uvicorn

# activate the same venv where you run DataEmbed.py
pip install --upgrade "langchain-community>=0.0.28"

```

## uses 
```sh
export PYTHONPATH=$PWD/src 
pip install -e .

python -m src.lm.Guardian tests/powershell/batch1/script_01.ps1
```
## run server
<!-- uvicorn src.api_scanbee:app --reload -->
```sh
export PYTHONPATH=$PWD/src     
uvicorn main:app --reload

chack port uses
lsof -i :8000
uvicorn main:app --reload

# 1. raw JSON
curl -X POST http://127.0.0.1:8000/analyze \
     -H "Content-Type: application/json" \
     -d '{"script": "Write-Host \"password is $pass\""}'

# 2. file upload
curl -X POST http://127.0.0.1:8000/analyze \
     -F "file=@tests/test.ps1"
```


## For huggingface show list of models installed 
```bash

# Summarize your entire cache
huggingface-cli scan-cache

# Add --verbose to list every repo revision
huggingface-cli scan-cache --verbose

# Machine-readable JSON
huggingface-cli scan-cache --json
rm -rf ~/.cache/huggingface/hub/models--mistralai--Mistral-7B-Instruct-v0.2


# update hugging face
pip install -U "huggingface_hub>=0.24" "transformers>=4.41"

# download a model
transformers-cli download mistralai/Mistral-7B-v0.1 --cache-dir /path/to/exports

# replace TOKEN with your real HF token string
HF_TOKEN=hf_xxxxx huggingface-cli download mistralai/Mistral-7B-v0.1 \
    --repo-type model \
    --local-dir ~/hf_cache/mistral-7b \
    --local-dir-use-symlinks auto            # only on hub ≥ 0.21


python download.py          # prompts for token
# or
HF_TOKEN=hf_xxx python download_mistral.py

```