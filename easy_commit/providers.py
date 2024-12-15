import openai
from groq import Groq
from anthropic import Anthropic
from together import Together
import cohere

SYSTEM_PROMPT = "You are a Git commit message generator. Create concise, descriptive commit messages."

def create_user_prompt(diff, max_length, optional_prompt):
    """Generate a standardized user prompt for commit message generation"""
    return f"""Generate a concise, one-line Git commit message based on these code changes. 
    Guidelines:
    - Short summary (max {max_length} characters)
    - Use imperative mood
    - Focus on the primary change
    - If staged changes contain multiple files, concisely summarize
    
    Code Diff: {diff}

    Additional Instructions: {optional_prompt or 'None'}
    
    Start directly with the commit message, nothing before or after it."""

def generate_openai_message(diff, api_key, model, max_length, optional_prompt):
    """Generate commit message using OpenAI API"""
    client = openai.OpenAI(api_key=api_key)
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": create_user_prompt(diff, max_length, optional_prompt)}
            ],
            temperature=0.6,
            max_tokens=max_length
        )
        return response.choices[0].message.content.strip()[:max_length]
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return ""

def generate_groq_message(diff, api_key, model, max_length, optional_prompt):
    """Generate commit message using Groq API"""
    client = Groq(api_key=api_key)
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": create_user_prompt(diff, max_length, optional_prompt)}
            ],
            model=model,
            temperature=0.6,
            max_tokens=max_length
        )
        return chat_completion.choices[0].message.content.strip()[:max_length]
    except Exception as e:
        print(f"Groq API Error: {e}")
        return ""

def generate_claude_message(diff, api_key, model, max_length, optional_prompt):
    """Generate commit message using Anthropic Claude API"""
    client = Anthropic(api_key=api_key)
    
    try:
        response = client.messages.create(
            model=model,
            max_tokens=max_length,
            temperature=0.6,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": create_user_prompt(diff, max_length, optional_prompt)}
            ]
        )
        return response.content[0].text.strip()[:max_length]
    except Exception as e:
        print(f"Claude API Error: {e}")
        return ""

def generate_together_message(diff, api_key, model, max_length, optional_prompt):
    """Generate commit message using Together AI API"""
    client = Together(api_key=api_key)
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": create_user_prompt(diff, max_length, optional_prompt)}
            ],
            temperature=0.6,
            max_tokens=max_length
        )
        return response.choices[0].message.content.strip()[:max_length]
    except Exception as e:
        print(f"Together AI API Error: {e}")
        return ""

def generate_cohere_message(diff, api_key, model, max_length, optional_prompt):
    """Generate commit message using Cohere API"""
    co = cohere.Client(api_key)
    
    try:
        response = co.generate(
            model=model,
            prompt=f"{SYSTEM_PROMPT}\n\n{create_user_prompt(diff, max_length, optional_prompt)}",
            max_tokens=max_length,
            temperature=0.6,
            k=0,
            stop_sequences=[],
            return_likelihoods='NONE'
        )
        return response.generations[0].text.strip()[:max_length]
    except Exception as e:
        print(f"Cohere API Error: {e}")
        return ""