```markdown
# Easy Commit

AI-powered Git commit message generator using Groq API.

## Installation

```bash
pip install easy-commit
```

## Usage

Set your Groq API key as an environment variable:
```bash
export GROQ_API_KEY=your_groq_api_key_here
```

Or pass it as a command-line argument:
```bash
easy-commit --api-key your_groq_api_key_here
```

Optional arguments:
- `--trunc-diff`: Maximum length of diff to analyze (default: 2048)
- `--commit-len`: Maximum length of commit message (default: 100)

## Requirements
- Python 3.7+
- Groq API key