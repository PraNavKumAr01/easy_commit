import argparse
import os
import subprocess
import shlex
from .generator import get_staged_diff, generate_commit_message

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Generate AI-powered Git commit messages')
    parser.add_argument('--trunc-diff', type=int, default=2048, 
                        help='Maximum length of diff to analyze (default: 2048)')
    parser.add_argument('--commit-len', type=int, default=100, 
                        help='Maximum length of commit message (default: 100)')
    parser.add_argument('--api-key', type=str, 
                        help='Groq API key (can also use GROQ_API_KEY env variable)')
    
    args = parser.parse_args()
    
    # Get API key from environment or argument
    api_key = args.api_key or os.environ.get('GROQ_API_KEY')
    if not api_key:
        print("Error: Groq API key not provided. Set GROQ_API_KEY environment variable or use --api-key.")
        return
    
    # Get staged diff
    diff = get_staged_diff(max_diff_length=args.trunc_diff)
    
    if not diff:
        print("No staged changes to commit.")
        return
    
    # Generate commit message
    commit_message = generate_commit_message(
        diff, 
        max_commit_length=args.commit_len, 
        api_key=api_key
    )
    
    if commit_message:
        try:
            # Construct the git commit command
            command = f"git commit -m {shlex.quote(commit_message)}"
            print(f"Command ready to run: {command}")
            
            # Prompt the user to confirm before running
            input("Press Enter to execute the command, or Ctrl+C to cancel...")
            
            # Execute the command
            subprocess.run(command, shell=True, check=True)
            print(f"Committed with message: {commit_message}")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
        except subprocess.CalledProcessError:
            print("Failed to commit. Please resolve any git issues.")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Could not generate a commit message.")