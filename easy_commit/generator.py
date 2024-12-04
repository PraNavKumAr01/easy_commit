import subprocess
from groq import Groq

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
        return "Staged Changes : " + staged_diff[:max_diff_length]
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving staged git diff: {e}")
        return ""

def generate_commit_message(diff, max_commit_length=100, api_key=None):
    """
    Generate a commit message based on staged git diff using Groq API.
    
    Args:
        diff (str): Git diff to analyze
        max_commit_length (int): Maximum length of commit message
        api_key (str): Groq API key
    
    Returns:
        str: Generated commit message
    """
    if not api_key:
        raise ValueError("Groq API key is required")
    
    client = Groq(api_key=api_key)
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a Git commit message generator. Create concise, descriptive commit messages."
                },
                {
                    "role": "user",
                    "content": f"""Generate a concise, one-line Git commit message based on these code changes. 
                    Guidelines:
                    - Short summary (max {max_commit_length} characters)
                    - Use imperative mood
                    - Focus on the primary change
                    - If staged changes contain multiple files, concisely summarize
                    
                    Code Diff: {diff}
                    
                    Start directly with the commit message, nothing before or after it."""
                }
            ],
            model="llama-3.1-8b-instant",
            temperature=0.6,
        )
        
        commit_message = chat_completion.choices[0].message.content.strip()
        
        # Truncate if needed
        return commit_message[:max_commit_length]
    
    except Exception as e:
        print(f"Error generating commit message: {e}")
        return ""