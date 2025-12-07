#!/usr/bin/env python3
"""
AI Python Code Generator
Uses Claude API to generate executable Python programs from prompts
"""

import json
import os
import subprocess
from datetime import datetime

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic library not installed.")
    print("Please run: pip install anthropic")
    exit(1)

API_KEY_FILE = '.code_generator_api_key.json'
GENERATION_LOG_FILE = 'code_generation_log.json'
OUTPUT_DIR = 'generated_programs'


def save_api_key(api_key):
    """Save API key to file"""
    with open(API_KEY_FILE, 'w') as f:
        json.dump({'api_key': api_key}, f)


def load_api_key():
    """Load API key from file"""
    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, 'r') as f:
            data = json.load(f)
            return data.get('api_key')
    return None


def get_api_key():
    """Get API key from file, environment variable, or user input"""
    api_key = load_api_key()
    
    if api_key:
        return api_key
    
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    
    if not api_key:
        print("\n" + "="*70)
        print("ANTHROPIC API KEY REQUIRED")
        print("="*70)
        print("You need an API key from: https://console.anthropic.com")
        print("Your API key will be saved securely for future use.")
        print("="*70)
        api_key = input("\nEnter your Anthropic API key: ").strip()
        
        if api_key:
            save_api_key(api_key)
            print("✓ API key saved successfully!")
    
    return api_key


def ensure_output_dir():
    """Create output directory if it doesn't exist"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def generate_code(prompt, api_key):
    """Generate Python code using Claude API"""
    client = anthropic.Anthropic(api_key=api_key)
    
    print(f"\n{'='*70}")
    print("GENERATING PYTHON CODE")
    print(f"{'='*70}")
    print("Claude is writing your program... This may take a moment.\n")
    
    full_prompt = f"""You are an expert Python programmer. Generate a complete, working Python program based on this request:

{prompt}

Requirements:
1. Write complete, executable Python code
2. Include proper error handling
3. Add clear comments explaining the code
4. Use best practices and clean code principles
5. Include a docstring at the top explaining what the program does
6. Make it user-friendly with clear prompts and output
7. Handle edge cases appropriately
8. If external libraries are needed, include import statements and note which libraries to install

Provide ONLY the Python code, no explanations before or after. The code should be ready to save and run immediately."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            messages=[
                {"role": "user", "content": full_prompt}
            ]
        )
        
        code = message.content[0].text
        
        # Remove markdown code blocks if present
        if code.startswith("```python"):
            code = code.split("```python", 1)[1]
            code = code.rsplit("```", 1)[0]
        elif code.startswith("```"):
            code = code.split("```", 1)[1]
            code = code.rsplit("```", 1)[0]
        
        code = code.strip()
        
        return code
    
    except anthropic.APIError as e:
        return f"# API Error: {str(e)}"
    except Exception as e:
        return f"# Error: {str(e)}"


def save_code(code, filename, prompt):
    """Save generated code to file"""
    ensure_output_dir()
    
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    with open(filepath, 'w') as f:
        f.write(code)
    
    # Make file executable
    os.chmod(filepath, 0o755)
    
    # Log generation
    log_generation(filename, prompt, filepath)
    
    return filepath


def log_generation(filename, prompt, filepath):
    """Log code generation to history"""
    log_data = []
    
    if os.path.exists(GENERATION_LOG_FILE):
        with open(GENERATION_LOG_FILE, 'r') as f:
            log_data = json.load(f)
    
    entry = {
        'filename': filename,
        'filepath': filepath,
        'prompt': prompt,
        'timestamp': datetime.now().isoformat()
    }
    
    log_data.append(entry)
    
    with open(GENERATION_LOG_FILE, 'w') as f:
        json.dump(log_data, f, indent=2)


def display_code(code, filepath):
    """Display generated code"""
    print(f"\n{'='*70}")
    print(f"CODE GENERATED SUCCESSFULLY")
    print(f"{'='*70}")
    print(f"Saved to: {filepath}")
    print(f"{'='*70}\n")
    print(code)
    print(f"\n{'='*70}")


def run_program(filepath):
    """Run the generated Python program"""
    print(f"\n{'='*70}")
    print(f"RUNNING: {filepath}")
    print(f"{'='*70}\n")
    
    try:
        result = subprocess.run(['python3', filepath], capture_output=False, text=True)
        print(f"\n{'='*70}")
        print(f"Program finished with exit code: {result.returncode}")
        print(f"{'='*70}")
    except Exception as e:
        print(f"\nError running program: {str(e)}")


def view_generated_programs():
    """View list of generated programs"""
    if not os.path.exists(GENERATION_LOG_FILE):
        print("\nNo programs generated yet.")
        return None
    
    with open(GENERATION_LOG_FILE, 'r') as f:
        log_data = json.load(f)
    
    if not log_data:
        print("\nNo programs generated yet.")
        return None
    
    print(f"\n{'='*70}")
    print("GENERATED PROGRAMS")
    print(f"{'='*70}")
    print(f"{'#':<5} {'Filename':<30} {'Date':<25}")
    print('-'*70)
    
    for i, entry in enumerate(reversed(log_data), 1):
        dt = datetime.fromisoformat(entry['timestamp'])
        filename = entry['filename'][:28] + '..' if len(entry['filename']) > 30 else entry['filename']
        print(f"{i:<5} {filename:<30} {dt.strftime('%b %d, %Y %I:%M %p'):<25}")
    
    print('='*70)
    
    return list(reversed(log_data))


def edit_program(filepath, api_key):
    """Edit an existing program with AI assistance"""
    if not os.path.exists(filepath):
        print(f"\nError: File '{filepath}' not found.")
        return
    
    # Read existing code
    with open(filepath, 'r') as f:
        existing_code = f.read()
    
    print(f"\n{'='*70}")
    print("CURRENT CODE:")
    print(f"{'='*70}\n")
    print(existing_code)
    print(f"\n{'='*70}")
    
    edit_prompt = input("\nWhat changes do you want to make? (or 'cancel' to go back): ").strip()
    
    if edit_prompt.lower() == 'cancel':
        print("Edit cancelled.")
        return
    
    client = anthropic.Anthropic(api_key=api_key)
    
    print("\nGenerating updated code...")
    
    full_prompt = f"""Here is an existing Python program:

```python
{existing_code}
```

Please modify this code according to this request:
{edit_prompt}

Provide the COMPLETE updated Python code (not just the changes). The code should be ready to run immediately.
Include all necessary imports, error handling, and maintain code quality."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            messages=[
                {"role": "user", "content": full_prompt}
            ]
        )
        
        new_code = message.content[0].text
        
        # Remove markdown code blocks if present
        if new_code.startswith("```python"):
            new_code = new_code.split("```python", 1)[1]
            new_code = new_code.rsplit("```", 1)[0]
        elif new_code.startswith("```"):
            new_code = new_code.split("```", 1)[1]
            new_code = new_code.rsplit("```", 1)[0]
        
        new_code = new_code.strip()
        
        # Save updated code
        with open(filepath, 'w') as f:
            f.write(new_code)
        
        print(f"\n✓ Code updated successfully!")
        display_code(new_code, filepath)
        
    except Exception as e:
        print(f"\nError updating code: {str(e)}")


def main():
    """Main function"""
    print("="*70)
    print("AI PYTHON CODE GENERATOR")
    print("Powered by Claude API")
    print("="*70)
    
    api_key = get_api_key()
    
    if not api_key:
        print("\nNo API key provided. Exiting.")
        return
    
    print("\n✓ API key loaded successfully!")
    ensure_output_dir()
    
    while True:
        print("\nOptions:")
        print("1. Generate new Python program")
        print("2. View generated programs")
        print("3. Run a generated program")
        print("4. Edit a generated program with AI")
        print("5. Delete saved API key")
        print("6. Exit")
        
        choice = input("\nSelect an option (1-6): ").strip()
        
        if choice == '1':
            print("\n" + "="*70)
            print("DESCRIBE YOUR PROGRAM")
            print("="*70)
            print("Examples:")
            print("- Create a calculator that handles basic math operations")
            print("- Build a todo list manager that saves to a file")
            print("- Make a password generator with customizable length")
            print("="*70)
            
            prompt = input("\nWhat program do you want to create?\n> ").strip()
            
            if not prompt:
                print("No prompt provided.")
                continue
            
            # Generate filename
            filename = input("\nEnter filename (e.g., calculator.py): ").strip()
            
            if not filename:
                # Generate automatic filename
                filename = f"program_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
                print(f"Using automatic filename: {filename}")
            elif not filename.endswith('.py'):
                filename += '.py'
            
            # Generate code
            code = generate_code(prompt, api_key)
            
            # Save code
            filepath = save_code(code, filename, prompt)
            
            # Display code
            display_code(code, filepath)
            
            print(f"\n✓ Program saved to: {filepath}")
            
            # Ask if user wants to run it
            run = input("\nRun the program now? (y/n): ").strip().lower()
            if run == 'y':
                run_program(filepath)
        
        elif choice == '2':
            programs = view_generated_programs()
            
            if programs:
                view_choice = input("\nEnter program number to view code (or press Enter to go back): ").strip()
                
                if view_choice.isdigit():
                    idx = int(view_choice) - 1
                    if 0 <= idx < len(programs):
                        entry = programs[idx]
                        filepath = entry['filepath']
                        
                        if os.path.exists(filepath):
                            with open(filepath, 'r') as f:
                                code = f.read()
                            display_code(code, filepath)
                        else:
                            print(f"\nFile not found: {filepath}")
        
        elif choice == '3':
            programs = view_generated_programs()
            
            if programs:
                run_choice = input("\nEnter program number to run: ").strip()
                
                if run_choice.isdigit():
                    idx = int(run_choice) - 1
                    if 0 <= idx < len(programs):
                        entry = programs[idx]
                        filepath = entry['filepath']
                        
                        if os.path.exists(filepath):
                            run_program(filepath)
                        else:
                            print(f"\nFile not found: {filepath}")
        
        elif choice == '4':
            programs = view_generated_programs()
            
            if programs:
                edit_choice = input("\nEnter program number to edit: ").strip()
                
                if edit_choice.isdigit():
                    idx = int(edit_choice) - 1
                    if 0 <= idx < len(programs):
                        entry = programs[idx]
                        filepath = entry['filepath']
                        edit_program(filepath, api_key)
        
        elif choice == '5':
            if os.path.exists(API_KEY_FILE):
                confirm = input("\nAre you sure you want to delete the saved API key? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    os.remove(API_KEY_FILE)
                    print("\n✓ API key deleted successfully!")
                    print("You will need to enter it again next time.")
                else:
                    print("\nDeletion cancelled.")
            else:
                print("\nNo saved API key found.")
        
        elif choice == '6':
            print("\nHappy coding! 🐍")
            break
        
        else:
            print("Invalid option. Please select 1-6.")


if __name__ == "__main__":
    main()
