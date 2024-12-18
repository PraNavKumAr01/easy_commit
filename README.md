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

### Save your default provider configuration
#### You can set the provider and api-key once when you first run it, after that you will be able to run it in any project or IDE.
```bash
easy-commit --provider groq --api-key your-api-key --save-config
```

Arguments:
- `--diff-size` : Maximum length of diff to analyze (default: 2048)
- `--trunc-diff`: Flag to include multiple diffs or truncate the diff (default: False) `use it when you can a lot of code changes, but be carefull as this might use a lot of tokens`
- `--commit-len`: Maximum length of commit message (default: 100)
- `--provider` :  API provider to use for LLM functionality (default: groq)
- `--api-key` : API key for the selected LLM provider
- `--save-config` : Flag to save the provided configuration of easier accesability later (default: False)

## Examples
```bash
easy-commit
```
Yes! Thats actually all it takes. You will be shown the commit message, and prompted to press enter to perform the commit

### With arguments
```bash
easy-commit --diff-size 1024 --commit-len 50 --provider groq --api-key your-api-key
```

## Requirements
- Python 3.7+
- Groq API key
