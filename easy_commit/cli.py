import argparse
import os
import subprocess
import shlex
import json
from .generator import get_staged_diff_chunks, generate_commit_message
from colorama import Fore, Style, init

CONFIG_PATH = os.path.expanduser("~/.config/easy_commit/config.json")

# Initialize colorama
init(autoreset=True)

def get_terminal_width():
    """Get the terminal width, default to 80 if unable to determine."""
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80

def create_box(message):
    """Create a box around the message using ASCII characters."""
    width = min(get_terminal_width() - 4, max(len(line) for line in message.split('\n')) + 4)
    horizontal_line = '─' * width
    box_top = f'╭{horizontal_line}╮'
    box_bottom = f'╰{horizontal_line}╯'
    
    # Wrap and pad the message
    wrapped_lines = []
    for line in message.split('\n'):
        while line:
            if len(line) <= width - 4:
                wrapped_lines.append(line)
                line = ''
            else:
                space_index = line[:width-4].rfind(' ')
                if space_index == -1:
                    wrapped_lines.append(line[:width-4])
                    line = line[width-4:]
                else:
                    wrapped_lines.append(line[:space_index])
                    line = line[space_index+1:]

    message_lines = [f'│  {line:<{width-4}}  │' for line in wrapped_lines]
    
    return '\n'.join([box_top, *message_lines, box_bottom])

def print_separator():
    """Print a separator line across the terminal width."""
    width = get_terminal_width()
    print(Fore.BLUE + '─' * width)

def load_config():
    """Load configuration from file."""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_config(provider_name, api_key):
    """Save configuration to file."""
    config = {"provider_name": provider_name, "api_key": api_key}
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

def extract_provider_name(provider):
    """Extract the provider name from the full provider string."""
    return provider.split('/')[0]

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Generate AI-powered Git commit messages')
    parser.add_argument('--trunc-diff', action='store_true',
                        help='Include all diffs or truncate to diff-size')
    parser.add_argument('--diff-size', type=int, default=2048, 
                        help='Maximum length of diff to analyze (default: 2048)')
    parser.add_argument('--commit-len', type=int, default=200, 
                        help='Maximum length of commit message (default: 150)')
    parser.add_argument('--provider', type=str, default="groq/llama-3.1-8b-instant",
                        help='Provider and Model Name (default: groq/llama-3.1-8b-instant)')
    parser.add_argument('--api-key', type=str, 
                        help='Provider API key (can also use PROVIDER_API_KEY env variable)')
    parser.add_argument('--save-config', action='store_true', 
                        help='Save provider and API key as default configuration')
    
    args = parser.parse_args()
    
    # Load existing config
    config = load_config()
    
    # Determine provider and API key
    provider = args.provider
    api_key = args.api_key
    
    # If no API key provided, check config
    if not api_key and config.get('provider_name') == extract_provider_name(provider):
        api_key = config.get('api_key')
    
    # Save config if requested and both provider and API key are provided
    if args.save_config and provider and api_key:
        save_config(extract_provider_name(provider), api_key)
        print(Fore.GREEN + f"Saved default configuration for provider: {provider}")
        print_separator()
    
    # Get staged diff
    diff = get_staged_diff_chunks(max_diff_length=args.diff_size)

    if args.trunc_diff:
        diff = diff[0]
    
    if not diff:
        print(Fore.RED + "No staged changes to commit.")
        return
    
    # Generate commit message
    commit_message = generate_commit_message(
        diff, 
        max_commit_length=args.commit_len, 
        api_key=api_key,
        provider=provider
    )
    
    while True:
        if commit_message:
            try:
                # Display the generated commit message in a box
                print(Fore.CYAN + create_box(commit_message))
                print_separator()
                
                # Prompt user for action in a single line
                action = input(Fore.YELLOW + "Press 'enter' to commit, 'c' to cancel, or 'r' to revise the message: ").strip().lower()
                print_separator()
                
                if action == '':
                    # Construct the git commit command
                    command = f"git commit -m {shlex.quote(commit_message)}"
                    print(Fore.GREEN + f"Command ready to run: {command}")
                    print_separator()
                    
                    # Execute the command
                    subprocess.run(command, shell=True, check=True)
                    print(Fore.GREEN + f"Committed with message: {commit_message}")
                    print_separator()
                    break
                
                elif action == 'c':
                    print(Fore.RED + "Operation cancelled.")
                    print_separator()
                    break
                
                elif action == 'r':
                    optional_prompt = input(Fore.YELLOW + "Enter your custom prompt for the commit message: ").strip()
                    print_separator()
                    commit_message = generate_commit_message(
                        diff, 
                        max_commit_length=args.commit_len, 
                        api_key=api_key,
                        provider=provider,
                        optional_prompt=optional_prompt
                    )
                
                else:
                    print(Fore.RED + "Invalid option. Please enter 'enter', 'c', or 'r'.")
                    print_separator()
            
            except subprocess.CalledProcessError:
                print(Fore.RED + "Failed to commit. Please resolve any git issues.")
                print_separator()
            except Exception as e:
                print(Fore.RED + f"An error occurred: {e}")
                print_separator()
        else:
            print(Fore.RED + "Could not generate a commit message.")
            print_separator()
            break