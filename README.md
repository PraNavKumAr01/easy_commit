# Easy Commit

AI-powered Git commit message generator using Groq API.

## Installation

```bash
pip install easy-commit
```

## Usage

### Stage your changes
```bash
git add .
```
It is neccesary to first stage all your changes. This picks up the code diffs from the staged changes.

### Set your Groq API key as an environment variable:
```bash
export GROQ_API_KEY=your_groq_api_key_here
```

### Or pass it as a command-line argument:
```bash
easy-commit --api-key your_groq_api_key_here
```

Optional arguments:
- `--trunc-diff`: Maximum length of diff to analyze (default: 2048)
- `--commit-len`: Maximum length of commit message (default: 100)

## Examples
```bash
easy-commit
```
Yes! Thats actually all it takes. You will be shown the commit message, and prompted to press enter to perform the commit

### With arguments
```bash
easy-commit --trunc-diff 1024 --commit-len 50 --model-name "llama3-8b-8192"
```

## Requirements
- Python 3.7+
- Groq API key