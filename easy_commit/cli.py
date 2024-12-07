import argparse
import os
import subprocess
import shlex
from generator import get_staged_diff, generate_commit_message

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Generate AI-powered Git commit messages')
    parser.add_argument('--trunc-diff', type=int, default=2048, 
                        help='Maximum length of diff to analyze (default: 2048)')
    parser.add_argument('--commit-len', type=int, default=100, 
                        help='Maximum length of commit message (default: 100)')
    parser.add_argument('--model-name', type=str, default = "llama-3.1-8b-instant",
                        help='Groq Model Name (default: llama-3.1-8b-instant)')
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
        api_key=api_key,
        model_name=args.model_name
    )
    
    while True:
        if commit_message:
            try:
                # Display the generated commit message
                print(f"Generated commit message: {commit_message}")
                
                # Prompt user for action
                action = input("Press 'enter' to commit, 'c' to cancel, or 'r' to revise the message: ").strip().lower()
                
                if action == 'enter':
                    # Construct the git commit command
                    command = f"git commit -m {shlex.quote(commit_message)}"
                    print(f"Command ready to run: {command}")
                    
                    # Execute the command
                    subprocess.run(command, shell=True, check=True)
                    print(f"Committed with message: {commit_message}")
                    break
                
                elif action == 'c':
                    print("Operation cancelled.")
                    break
                
                elif action == 'r':
                    optional_prompt = input("Enter your custom prompt for the commit message: ").strip()
                    commit_message = generate_commit_message(
                        diff, 
                        max_commit_length=args.commit_len, 
                        api_key=api_key,
                        model_name=args.model_name,
                        optional_prompt=optional_prompt
                    )
                
                else:
                    print("Invalid option. Please enter 'enter', 'c', or 'r'.")
            
            except subprocess.CalledProcessError:
                print("Failed to commit. Please resolve any git issues.")
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print("Could not generate a commit message.")
            break