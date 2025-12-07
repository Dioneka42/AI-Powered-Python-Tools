#!/usr/bin/env python3
"""
Stock Research Assistant
Automated company analysis using Claude API
"""

import json
import os
from datetime import datetime

# NOTE: You need to install the anthropic library first:
# pip install anthropic

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic library not installed.")
    print("Please run: pip install anthropic")
    exit(1)

# Research questions to ask about each stock
RESEARCH_QUESTIONS = [
    "How are the earnings?",
    "What are the profit margins?",
    "How are the cash flows?",
    "What are the expenses like?",
    "What is the company forecasting?",
    "Is their management competent? Does the CEO know what he or she is doing?",
    "Does it have scale? Has it grown into a market leader?",
    "Does it have influence on the market such that it can call the shots to its suppliers?",
    "Is there a lot of staff turnover?",
    "Does it have good benefits for employees?",
    "Are the conference calls going well with analysts?",
    "Do people like working there? Do they have good benefits for working there?",
    "Does it have a protective technological moat?",
    "Can it grow fast and continue to invent and reinvent as superb companies do?"
]

RESEARCH_LOG_FILE = 'stock_research_log.json'
API_KEY_FILE = '.api_key.json'


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
    # Try to load from file first
    api_key = load_api_key()
    
    if api_key:
        return api_key
    
    # Try environment variable
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


def research_company(ticker, api_key):
    """Research a company using Claude API"""
    client = anthropic.Anthropic(api_key=api_key)
    
    print(f"\n{'='*70}")
    print(f"RESEARCHING: {ticker.upper()}")
    print(f"{'='*70}")
    print("Conducting deep analysis... This may take a moment.\n")
    
    # Construct comprehensive prompt with emphasis on depth
    prompt = f"""Please provide an exceptionally detailed and comprehensive analysis of {ticker.upper()}. I need deep insights, not surface-level information. For each aspect below, provide substantial detail with specific data, examples, trends, and context:

1. **Earnings Performance**: Provide detailed earnings trends over the past 3-5 years, including quarterly performance, year-over-year growth rates, earnings surprises (beats/misses), and any notable patterns or inflection points. Discuss revenue breakdown by segment if applicable.

2. **Profit Margins**: Analyze gross, operating, and net profit margins in detail. Compare to industry averages and competitors. Discuss margin trends, expansion or contraction, and the underlying drivers (pricing power, cost management, economies of scale, etc.).

3. **Cash Flows**: Deep dive into operating cash flow, free cash flow, and cash flow conversion rates. Analyze the quality of earnings through cash flow analysis. Discuss capital expenditure needs, working capital trends, and cash generation efficiency.

4. **Expense Structure**: Break down the expense categories (COGS, R&D, SG&A, etc.). Identify where the company is spending money and whether this spending is efficient. Discuss any cost-cutting initiatives or areas of concern.

5. **Company Forecasts and Guidance**: Detail management's forward guidance, analyst expectations, and any discrepancies between the two. Discuss the company's historical accuracy in meeting guidance and any factors that might impact future projections.

6. **Management Competence and CEO Leadership**: Provide a thorough assessment of the management team's track record, strategic vision, capital allocation decisions, and leadership effectiveness. Include the CEO's background, tenure, major decisions, and how they're perceived by analysts and investors.

7. **Market Scale and Leadership Position**: Analyze the company's market share, competitive positioning, and whether it's a market leader, challenger, or niche player. Discuss barriers to entry, competitive advantages, and the overall market dynamics.

8. **Market Influence and Supplier Relationships**: Assess the company's bargaining power with suppliers and customers. Does it have pricing power? Can it dictate terms? Discuss the supply chain dynamics and any potential vulnerabilities or strengths.

9. **Employee Turnover Rates**: Provide specific data on turnover rates if available, compare to industry benchmarks, and discuss what this indicates about company culture and stability. Include any recent trends or concerns.

10. **Employee Benefits and Compensation**: Detail the compensation packages, benefits, equity programs, and how they compare to competitors. Discuss whether the company is seen as an employer of choice in its industry.

11. **Analyst Conference Call Reception**: Analyze how recent earnings calls have been received. What questions are analysts asking? Are there recurring concerns? How transparent and forthcoming is management?

12. **Employee Satisfaction and Workplace Culture**: Provide insights from employee reviews (Glassdoor, etc.), company culture initiatives, work-life balance reputation, and overall sentiment about working there. Include specific examples or quotes if available.

13. **Technological Moat and Competitive Advantages**: Conduct a deep analysis of the company's sustainable competitive advantages. What makes it hard to replicate? Patents, network effects, brand power, switching costs, proprietary technology, etc. Be specific about the strength and durability of these moats.

14. **Innovation Capacity and Growth Potential**: Assess the company's R&D capabilities, track record of innovation, ability to adapt to market changes, and potential for continued growth. Discuss new products/services in development, expansion opportunities, and strategic initiatives.

Please be thorough and specific. Include numbers, percentages, comparisons, and concrete examples wherever possible. Cite recent data and sources. I want a report that gives me deep understanding, not just overview-level information. Each section should be multiple paragraphs with substantial detail."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,  # Increased for longer, more detailed responses
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response = message.content[0].text
        return response
    
    except anthropic.APIError as e:
        return f"API Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


def save_research(ticker, research_data):
    """Save research to log file"""
    log_data = []
    
    if os.path.exists(RESEARCH_LOG_FILE):
        with open(RESEARCH_LOG_FILE, 'r') as f:
            log_data = json.load(f)
    
    research_entry = {
        'ticker': ticker.upper(),
        'timestamp': datetime.now().isoformat(),
        'research': research_data
    }
    
    log_data.append(research_entry)
    
    with open(RESEARCH_LOG_FILE, 'w') as f:
        json.dump(log_data, f, indent=2)


def display_research(ticker, research):
    """Display research results"""
    print(f"\n{'='*70}")
    print(f"RESEARCH REPORT: {ticker.upper()}")
    print(f"Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    print(f"{'='*70}\n")
    print(research)
    print(f"\n{'='*70}")


def view_past_research():
    """View past research reports"""
    if not os.path.exists(RESEARCH_LOG_FILE):
        print("\nNo past research found.")
        return
    
    with open(RESEARCH_LOG_FILE, 'r') as f:
        log_data = json.load(f)
    
    if not log_data:
        print("\nNo past research found.")
        return
    
    print(f"\n{'='*70}")
    print("PAST RESEARCH REPORTS")
    print(f"{'='*70}")
    print(f"{'#':<5} {'Ticker':<10} {'Date':<30}")
    print('-'*70)
    
    for i, entry in enumerate(reversed(log_data), 1):
        dt = datetime.fromisoformat(entry['timestamp'])
        print(f"{i:<5} {entry['ticker']:<10} {dt.strftime('%b %d, %Y %I:%M %p'):<30}")
    
    print('='*70)
    
    choice = input("\nEnter report number to view (or press Enter to go back): ").strip()
    
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(log_data):
            entry = list(reversed(log_data))[idx]
            display_research(entry['ticker'], entry['research'])
        else:
            print("Invalid selection.")


def export_research_to_file(ticker, research):
    """Export research to a text file"""
    filename = f"{ticker.upper()}_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, 'w') as f:
        f.write(f"STOCK RESEARCH REPORT: {ticker.upper()}\n")
        f.write(f"Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")
        f.write("="*70 + "\n\n")
        f.write(research)
        f.write("\n\n" + "="*70 + "\n")
        f.write("Generated by Stock Research Assistant\n")
    
    print(f"\n✓ Research exported to: {filename}")


def main():
    """Main function"""
    print("="*70)
    print("STOCK RESEARCH ASSISTANT")
    print("Powered by Claude API - Deep Analysis Mode")
    print("="*70)
    
    # Get API key
    api_key = get_api_key()
    
    if not api_key:
        print("\nNo API key provided. Exiting.")
        return
    
    while True:
        print("\nOptions:")
        print("1. Research a stock")
        print("2. View past research")
        print("3. Clear saved API key")
        print("4. Exit")
        
        choice = input("\nSelect an option (1-4): ").strip()
        
        if choice == '1':
            ticker = input("\nEnter stock ticker or company name: ").strip()
            
            if not ticker:
                print("Please enter a valid ticker.")
                continue
            
            research = research_company(ticker, api_key)
            display_research(ticker, research)
            
            # Save research
            save_research(ticker, research)
            print("\n✓ Research saved to log!")
            
            # Ask if user wants to export
            export = input("\nExport to text file? (y/n): ").strip().lower()
            if export == 'y':
                export_research_to_file(ticker, research)
        
        elif choice == '2':
            view_past_research()
        
        elif choice == '3':
            if os.path.exists(API_KEY_FILE):
                os.remove(API_KEY_FILE)
                print("\n✓ API key cleared!")
            else:
                print("\nNo saved API key found.")
        
        elif choice == '4':
            print("\nThank you for using Stock Research Assistant!")
            break
        
        else:
            print("Invalid option. Please select 1-4.")


if __name__ == "__main__":
    main()
