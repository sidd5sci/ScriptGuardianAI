# ScriptGuardian

Offline security‑issue detector for PowerShell & Groovy scripts.  
Uses a *local* LLM (Mistral, Claude Sonnet via Ollama, etc.) plus a **vector store** of labelled examples for k‑shot RAG.

## future scope
* Can alayse script behaviour (give error for prohebited opration under core data sources, such as kill a proccess, modify file)
* Give Code suggation for error and warning lines 
* Reccomanded  opration 
* file upload analysis for datasources and modules
* 
*

## Quick start

```bash
git clone <repo>
cd Script Guardian

brew update
brew install pyenv
brew install pyenv-virtualenv

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
# Load pyenv-virtualenv into the shell
eval "$(pyenv virtualenv-init -)"


pyenv install 3.12.3
pyenv virtualenv 3.12.3 guardian

source ~/.zshrc
pyenv activate guardian

pip install -r requirements.txt
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



# activate the same venv where you run DataEmbed.py
```sh
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

