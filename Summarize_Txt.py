#!/usr/bin/env python3
"""
Text File Summarizer
Analyzes .txt files and generates bullet point summaries using Claude API
"""

import json
import os
from datetime import datetime

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic library not installed.")
    print("Please run: pip install anthropic")
    exit(1)

API_KEY_FILE = '.summarizer_api_key.json'
SUMMARY_LOG_FILE = 'summary_log.json'


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


def read_text_file(filepath):
    """Read content from a text file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"\nError: File '{filepath}' not found.")
        return None
    except Exception as e:
        print(f"\nError reading file: {str(e)}")
        return None


def summarize_text(content, filename, summary_type, api_key):
    """Summarize text content using Claude API"""
    client = anthropic.Anthropic(api_key=api_key)
    
    print(f"\n{'='*70}")
    print(f"SUMMARIZING: {filename}")
    print(f"{'='*70}")
    print("Analyzing and creating bullet point summary...\n")
    
    prompts = {
        'concise': f"""Please read the following text and provide a CONCISE bullet point summary.

Extract the most important points and present them as clear, actionable bullet points. Focus on key takeaways, main ideas, and critical information.

Keep it brief but comprehensive - aim for 5-10 main bullet points.

TEXT TO SUMMARIZE:
{content}""",
        
        'detailed': f"""Please read the following text and provide a DETAILED bullet point summary.

Break down the content into comprehensive bullet points that cover:
- Main themes and arguments
- Key facts and data points
- Important details and context
- Conclusions and implications

Organize into categories if the content covers multiple topics. Use sub-bullets where appropriate.

TEXT TO SUMMARIZE:
{content}""",
        
        'key_points': f"""Please read the following text and extract the KEY POINTS ONLY.

Identify and list:
- The most critical takeaways
- Essential facts or figures
- Main conclusions or recommendations
- Action items (if any)

Present as a prioritized list with the most important points first. Be extremely focused - only include what's truly essential.

TEXT TO SUMMARIZE:
{content}""",
        
        'executive': f"""Please read the following text and provide an EXECUTIVE SUMMARY in bullet point format.

Create a high-level overview suitable for quick decision-making:
- Bottom-line up front (BLUF) - what's the key message?
- Main findings or results
- Critical data or metrics
- Recommendations or next steps

Format for busy executives who need the essential information quickly.

TEXT TO SUMMARIZE:
{content}"""
    }
    
    prompt = prompts.get(summary_type, prompts['detailed'])
    
    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        summary = message.content[0].text
        return summary
    
    except anthropic.APIError as e:
        return f"API Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


def display_summary(filename, summary):
    """Display the summary"""
    print(f"\n{'='*70}")
    print(f"SUMMARY: {filename}")
    print(f"Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    print(f"{'='*70}\n")
    print(summary)
    print(f"\n{'='*70}")


def save_summary(filename, original_content, summary, summary_type):
    """Save summary to log file"""
    log_data = []
    
    if os.path.exists(SUMMARY_LOG_FILE):
        with open(SUMMARY_LOG_FILE, 'r') as f:
            log_data = json.load(f)
    
    entry = {
        'filename': filename,
        'timestamp': datetime.now().isoformat(),
        'summary_type': summary_type,
        'original_length': len(original_content),
        'summary': summary
    }
    
    log_data.append(entry)
    
    with open(SUMMARY_LOG_FILE, 'w') as f:
        json.dump(log_data, f, indent=2)


def export_summary(filename, summary):
    """Export summary to a new text file"""
    base_name = os.path.splitext(filename)[0]
    output_filename = f"{base_name}_SUMMARY_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(output_filename, 'w') as f:
        f.write(f"BULLET POINT SUMMARY\n")
        f.write(f"Original File: {filename}\n")
        f.write(f"Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")
        f.write("="*70 + "\n\n")
        f.write(summary)
        f.write("\n\n" + "="*70 + "\n")
        f.write("Generated by Text File Summarizer\n")
    
    print(f"\n✓ Summary exported to: {output_filename}")


def view_past_summaries():
    """View past summaries"""
    if not os.path.exists(SUMMARY_LOG_FILE):
        print("\nNo past summaries found.")
        return
    
    with open(SUMMARY_LOG_FILE, 'r') as f:
        log_data = json.load(f)
    
    if not log_data:
        print("\nNo past summaries found.")
        return
    
    print(f"\n{'='*70}")
    print("PAST SUMMARIES")
    print(f"{'='*70}")
    print(f"{'#':<5} {'Filename':<30} {'Type':<15} {'Date':<20}")
    print('-'*70)
    
    for i, entry in enumerate(reversed(log_data), 1):
        dt = datetime.fromisoformat(entry['timestamp'])
        filename = entry['filename'][:28] + '..' if len(entry['filename']) > 30 else entry['filename']
        print(f"{i:<5} {filename:<30} {entry['summary_type']:<15} {dt.strftime('%b %d, %Y %I:%M %p'):<20}")
    
    print('='*70)
    
    choice = input("\nEnter summary number to view (or press Enter to go back): ").strip()
    
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(log_data):
            entry = list(reversed(log_data))[idx]
            display_summary(entry['filename'], entry['summary'])
        else:
            print("Invalid selection.")


def list_txt_files():
    """List all .txt files in current directory"""
    txt_files = [f for f in os.listdir('.') if f.endswith('.txt')]
    
    if not txt_files:
        print("\nNo .txt files found in current directory.")
        return None
    
    print(f"\n{'='*70}")
    print("AVAILABLE TEXT FILES")
    print(f"{'='*70}")
    
    for i, filename in enumerate(txt_files, 1):
        size = os.path.getsize(filename)
        size_kb = size / 1024
        print(f"{i}. {filename} ({size_kb:.1f} KB)")
    
    print('='*70)
    
    return txt_files


def main():
    """Main function"""
    print("="*70)
    print("TEXT FILE SUMMARIZER")
    print("Powered by Claude API")
    print("="*70)
    
    api_key = get_api_key()
    
    if not api_key:
        print("\nNo API key provided. Exiting.")
        return
    
    print("\n✓ API key loaded successfully!")
    
    while True:
        print("\nOptions:")
        print("1. Summarize a text file")
        print("2. View past summaries")
        print("3. Delete saved API key")
        print("4. Exit")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == '1':
            # Show available files or let user enter path
            print("\nWould you like to:")
            print("1. Choose from files in current directory")
            print("2. Enter a file path manually")
            
            file_choice = input("\nSelect (1-2): ").strip()
            
            filepath = None
            
            if file_choice == '1':
                txt_files = list_txt_files()
                if txt_files:
                    file_num = input("\nEnter file number: ").strip()
                    if file_num.isdigit() and 1 <= int(file_num) <= len(txt_files):
                        filepath = txt_files[int(file_num) - 1]
            elif file_choice == '2':
                filepath = input("\nEnter file path: ").strip()
            
            if not filepath:
                print("No file selected.")
                continue
            
            # Read the file
            content = read_text_file(filepath)
            if not content:
                continue
            
            print(f"\nFile loaded: {len(content)} characters")
            
            # Choose summary type
            print("\nSummary type:")
            print("1. Concise (5-10 key points)")
            print("2. Detailed (comprehensive breakdown)")
            print("3. Key points only (critical takeaways)")
            print("4. Executive summary (high-level overview)")
            
            summary_choice = input("\nSelect type (1-4, default=2): ").strip() or '2'
            
            summary_types = {
                '1': 'concise',
                '2': 'detailed',
                '3': 'key_points',
                '4': 'executive'
            }
            
            summary_type = summary_types.get(summary_choice, 'detailed')
            
            # Generate summary
            summary = summarize_text(content, filepath, summary_type, api_key)
            display_summary(filepath, summary)
            
            # Save summary
            save_summary(filepath, content, summary, summary_type)
            print("\n✓ Summary saved to log!")
            
            # Export option
            export = input("\nExport summary to new file? (y/n): ").strip().lower()
            if export == 'y':
                export_summary(filepath, summary)
        
        elif choice == '2':
            view_past_summaries()
        
        elif choice == '3':
            if os.path.exists(API_KEY_FILE):
                confirm = input("\nAre you sure you want to delete the saved API key? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    os.remove(API_KEY_FILE)
                    print("\n✓ API key deleted successfully!")
                    print("You will need to enter it again next time you run the program.")
                else:
                    print("\nDeletion cancelled.")
            else:
                print("\nNo saved API key found.")
        
        elif choice == '4':
            print("\nThank you for using Text File Summarizer!")
            break
        
        else:
            print("Invalid option. Please select 1-4.")


if __name__ == "__main__":
    main()
