import subprocess
from tqdm import tqdm
from .providers import generate_claude_message, generate_groq_message, generate_openai_message, generate_cohere_message, generate_together_message

def get_staged_diff(max_diff_length=2048):
    """
    Retrieve git diff for staged changes only.
    
    Args:
        max_diff_length (int): Maximum length of diff to retrieve
    
    Returns:
        str: Formatted git diff output for staged changes
    """
    try:
        staged_diff = subprocess.check_output(['git', 'diff', '--staged'], 
                                              stderr=subprocess.STDOUT, 
                                              text=True)
        return ["Staged Changes : " + staged_diff[:max_diff_length]]
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving staged git diff: {e}")
        return ""
    
def get_staged_diff_chunks(max_diff_length=2048, overlap=100):
    """
    Retrieve git diff for staged changes and split into chunks with overlap.
    
    Args:
        max_diff_length (int): Maximum length of each diff chunk
        overlap (int): Number of characters to overlap between chunks
    
    Returns:
        list: List of diff chunks with overlapping context
    """
    try:
        staged_diff = subprocess.check_output(['git', 'diff', '--staged'], 
                                              stderr=subprocess.STDOUT, 
                                              text=True)
        
        if not staged_diff:
            return []
        
        diff_chunks = []
        for i in range(0, len(staged_diff), max_diff_length - (2 * overlap)):
            # Calculate start and end indices with overlap
            start = max(0, i - overlap)
            end = min(i + max_diff_length, len(staged_diff))
            
            chunk = staged_diff[start:end]
            diff_chunks.append(chunk)
        
        return diff_chunks
    
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving staged git diff: {e}")
        return []
    
def generate_commit_message(diffs, max_commit_length=100, api_key=None, provider="groq", optional_prompt=None):
    """
    Generate a commit message based on staged git diff using multiple AI providers.
    
    Args:
        diff (str): Git diff to analyze
        max_commit_length (int): Maximum length of commit message
        api_key (str): API key for the selected provider
        provider (str): AI provider and model (e.g., "openai", "openai/gpt-3.5-turbo", 
                        "groq", "groq/llama-3.1-8b-instant", "claude", "claude/claude-3-haiku")
        optional_prompt (str, optional): Additional user instructions
    
    Returns:
        str: Generated commit message
    """

    # Default provider configurations
    provider_configs = {
        'openai': {
            'model': 'gpt-3.5-turbo',
            'api_func': generate_openai_message,
            'api_key_env': 'OPENAI_API_KEY'
        },
        'groq': {
            'model': 'llama-3.1-8b-instant',
            'api_func': generate_groq_message,
            'api_key_env': 'GROQ_API_KEY'
        },
        'claude': {
            'model': 'claude-3-haiku-20240307',
            'api_func': generate_claude_message,
            'api_key_env': 'ANTHROPIC_API_KEY'
        },
        'together': {
            'model': 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo',
            'api_func': generate_together_message,
            'api_key_env': 'TOGETHER_API_KEY'
        },
        'cohere': {
            'model': 'command-r-plus-08-2024',
            'api_func': generate_cohere_message,
            'api_key_env': 'COHERE_API_KEY'
        }
    }

    # Parse provider and model
    parts = provider.lower().split('/', 1)
    base_provider = parts[0]
    
    if base_provider not in provider_configs:
        raise ValueError(f"Unsupported provider: {base_provider}")
    
    # Use specific model if provided, otherwise use default
    model = parts[1] if len(parts) > 1 else provider_configs[base_provider]["model"]
    
    # Validate API key
    if not api_key:
        import os
        api_key = os.getenv(provider_configs[base_provider]["api_key_env"])
        if not api_key:
            raise ValueError(f"API key required for {base_provider}. Pass directly with --api-key or set environment variable.")

    # Generate commit message using appropriate provider
    config = provider_configs[base_provider]
    
    if len(diffs) > 1:

        temp_commit_messages = []

        for diff in tqdm(diffs, desc='Analysing Diffs'):
            commit_message =  config['api_func'](
                diff=diff, 
                api_key=api_key, 
                model=model, 
                max_length=max_commit_length, 
                optional_prompt=optional_prompt,
            )

            temp_commit_messages.append(commit_message)

        return config['api_func'](
            diff=temp_commit_messages, 
            api_key=api_key, 
            model=model, 
            max_length=max_commit_length, 
            optional_prompt=optional_prompt,
        ) 

    else:
    
        return config['api_func'](
            diff=diffs, 
            api_key=api_key, 
            model=model, 
            max_length=max_commit_length, 
            optional_prompt=optional_prompt,
        )