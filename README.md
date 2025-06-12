# ScaningBee

Offline security‑issue detector for PowerShell & Groovy scripts.  
Uses a *local* LLM (Mistral, Claude Sonnet via Ollama, etc.) plus a **vector store** of labelled examples for k‑shot RAG.

## Quick start

```bash
git clone <repo>
cd ScaningBee

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
pyenv virtualenv 3.10.13 bee-env

source ~/.zshrc
pyenv activate bee-env

pip3 install -r requirements.txt
```

other way 
```sh
python -m venv .venv && source .venv/bin/activate
pip install -e .
```
## start ollama 
```bash
ollama pull nomic-embed-text
ollama serve
```

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

pip3 install requests beautifulsoup4


pip3 install fastapi uvicorn

# activate the same venv where you run DataEmbed.py
pip install --upgrade "langchain-community>=0.0.28"

```

## uses 
```sh
export PYTHONPATH=$PWD/src 
pip install -e .
python -m Ollama.scanBee2 tests/test.ps1

python src/ollama/DataEmbed.py /Users/siddhartha.singh/scaningBee/resources
python src/ollama/ScanBee.py /Users/siddhartha.singh/scaningBee/tests/test.ps1
```
## run server
<!-- uvicorn src.api_scanbee:app --reload -->
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
