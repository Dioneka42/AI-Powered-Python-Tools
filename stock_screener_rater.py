#!/usr/bin/env python3
"""
AI Stock Screener & Rating System
Evaluates stocks against comprehensive criteria and provides 1-10 ratings
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

API_KEY_FILE = '.stock_screener_api_key.json'
RATING_LOG_FILE = 'stock_ratings_log.json'

# Evaluation criteria based on your research questions
EVALUATION_CRITERIA = """
FINANCIAL HEALTH (25 points):
- Strong earnings growth and consistency
- Healthy profit margins (gross, operating, net)
- Positive and growing cash flows
- Efficient expense management
- Manageable debt levels

MANAGEMENT & LEADERSHIP (15 points):
- Competent, experienced management team
- CEO with proven track record
- Clear strategic vision
- Good capital allocation decisions
- Transparent communication with investors

COMPETITIVE POSITION (20 points):
- Market leadership or strong position
- Significant scale advantages
- Pricing power and supplier leverage
- Strong technological moat
- Sustainable competitive advantages

GROWTH & INNOVATION (15 points):
- Strong growth potential
- Capacity for innovation and reinvention
- R&D investment and pipeline
- Market expansion opportunities
- Adaptability to change

COMPANY CULTURE (10 points):
- Low employee turnover
- Good employee benefits and compensation
- Positive workplace culture
- Strong employer reputation
- Employee satisfaction

ANALYST & MARKET SENTIMENT (10 points):
- Positive analyst conference call reception
- Strong institutional support
- Reasonable valuation
- Positive forward guidance
- Market confidence

RISK FACTORS (5 points):
- Manageable risks and challenges
- Geographic/customer diversification
- Regulatory compliance
- Supply chain stability
"""


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


def rate_stock(ticker, api_key):
    """Rate a specific stock on a 1-10 scale"""
    client = anthropic.Anthropic(api_key=api_key)
    
    print(f"\n{'='*70}")
    print(f"RATING: {ticker.upper()}")
    print(f"{'='*70}")
    print("Analyzing stock against comprehensive criteria...")
    print("This may take 3-5 minutes.\n")
    
    prompt = f"""You are an expert stock analyst. Provide a comprehensive evaluation and rating of {ticker.upper()} based on the following criteria:

{EVALUATION_CRITERIA}

Please provide a detailed analysis covering:

1. **FINANCIAL HEALTH ANALYSIS** (Out of 25 points)
   - Earnings: Recent performance, growth trends, consistency, beats/misses
   - Profit Margins: Gross, operating, and net margins vs. industry averages
   - Cash Flows: Operating cash flow, free cash flow, quality of earnings
   - Expenses: Cost structure, efficiency, any concerning trends
   - Overall Financial Health Score: X/25 points

2. **MANAGEMENT & LEADERSHIP** (Out of 15 points)
   - Management Competence: Track record, experience, decision-making
   - CEO Leadership: Background, tenure, strategic vision, capital allocation
   - Communication: Transparency, guidance accuracy, investor relations
   - Overall Management Score: X/15 points

3. **COMPETITIVE POSITION** (Out of 20 points)
   - Market Position: Market share, leadership status, competitive standing
   - Scale: Size advantages, economies of scale
   - Market Influence: Pricing power, supplier/customer relationships
   - Moat: Technological advantages, barriers to entry, sustainable advantages
   - Overall Competitive Position Score: X/20 points

4. **GROWTH & INNOVATION** (Out of 15 points)
   - Growth Potential: Revenue/earnings growth prospects, market opportunities
   - Innovation Capacity: R&D spending, new products/services, adaptability
   - Reinvention: Ability to evolve with market changes
   - Company Forecasts: Management guidance and analyst expectations
   - Overall Growth & Innovation Score: X/15 points

5. **COMPANY CULTURE** (Out of 10 points)
   - Employee Turnover: Rates compared to industry
   - Benefits & Compensation: Quality relative to competitors
   - Workplace Culture: Employee satisfaction, reviews (Glassdoor, etc.)
   - Employer Reputation: Ability to attract/retain talent
   - Overall Culture Score: X/10 points

6. **ANALYST & MARKET SENTIMENT** (Out of 10 points)
   - Conference Calls: Analyst reception, questions, concerns
   - Institutional Support: Major holders, recent activity
   - Valuation: Current valuation vs. historical and peers
   - Market Confidence: Sentiment, momentum, forward outlook
   - Overall Sentiment Score: X/10 points

7. **RISK ASSESSMENT** (Out of 5 points)
   - Key Risks: Major challenges or red flags
   - Risk Mitigation: How well positioned to handle risks
   - Overall Risk Score: X/5 points

---

**FINAL RATING:**
Total Score: X/100 points

**Overall Rating: X/10**

**RECOMMENDATION:**
- **BUY (8-10)**: Strong buy with high confidence
- **HOLD (6-7.9)**: Solid company, good for holding
- **NEUTRAL (5-5.9)**: Mixed signals, proceed with caution
- **AVOID (1-4.9)**: Significant concerns, not recommended

**Investment Recommendation:** [BUY/HOLD/NEUTRAL/AVOID]

**Key Strengths:** (3-5 bullet points)

**Key Concerns:** (3-5 bullet points)

**Bottom Line:** (2-3 sentence summary of whether this is a good investment and why)

**Currency Note:** Specify what currency the company reports earnings in (USD, CAD, EUR, etc.)

Please be thorough, honest, and data-driven in your analysis. Include specific numbers and comparisons where available."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        rating = message.content[0].text
        return rating
    
    except anthropic.APIError as e:
        return f"API Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


def screen_stocks(criteria_prompt, api_key):
    """Screen for stocks that meet specific criteria"""
    client = anthropic.Anthropic(api_key=api_key)
    
    print(f"\n{'='*70}")
    print(f"SCREENING FOR STOCKS")
    print(f"{'='*70}")
    print("Finding stocks that match your criteria...")
    print("This may take 3-5 minutes.\n")
    
    prompt = f"""You are an expert stock screener. Based on these criteria and preferences, recommend 5-10 stocks that best fit:

USER CRITERIA:
{criteria_prompt}

EVALUATION FRAMEWORK:
{EVALUATION_CRITERIA}

Please provide:

1. **RECOMMENDED STOCKS** (5-10 stocks)
   For each stock, provide:
   - Ticker symbol and company name
   - Brief description (1-2 sentences)
   - Why it fits the criteria
   - Quick rating estimate (X/10)
   - Current price range
   - Key strength that makes it stand out

2. **TOP 3 PICKS**
   Identify your top 3 recommendations with more detail:
   - Why this is a top pick
   - What makes it special
   - Risk factors to consider
   - Price target or valuation perspective

3. **DIVERSIFICATION NOTES**
   - How these picks work together
   - Sector/industry balance
   - Risk diversification

4. **WHAT TO WATCH**
   - Key metrics to monitor for these stocks
   - Upcoming catalysts or events
   - Risk factors across the group

Focus on stocks that genuinely meet the criteria with strong fundamentals. Be specific about why each stock qualifies. Include a mix of well-known and potentially undervalued names."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=8000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        recommendations = message.content[0].text
        return recommendations
    
    except anthropic.APIError as e:
        return f"API Error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


def display_rating(ticker, rating):
    """Display stock rating"""
    print(f"\n{'='*70}")
    print(f"STOCK RATING: {ticker.upper()}")
    print(f"Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    print(f"{'='*70}\n")
    print(rating)
    print(f"\n{'='*70}")


def save_rating(ticker, rating, rating_type):
    """Save rating to log file"""
    log_data = []
    
    if os.path.exists(RATING_LOG_FILE):
        with open(RATING_LOG_FILE, 'r') as f:
            log_data = json.load(f)
    
    entry = {
        'ticker': ticker.upper() if ticker else 'SCREEN',
        'rating_type': rating_type,
        'timestamp': datetime.now().isoformat(),
        'rating': rating
    }
    
    log_data.append(entry)
    
    with open(RATING_LOG_FILE, 'w') as f:
        json.dump(log_data, f, indent=2)


def export_rating(ticker, rating):
    """Export rating to text file"""
    filename = f"{ticker.upper()}_rating_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(filename, 'w') as f:
        f.write(f"STOCK RATING: {ticker.upper()}\n")
        f.write(f"Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")
        f.write("="*70 + "\n\n")
        f.write(rating)
        f.write("\n\n" + "="*70 + "\n")
        f.write("Generated by AI Stock Screener & Rating System\n")
    
    print(f"\n✓ Rating exported to: {filename}")


def view_past_ratings():
    """View past ratings"""
    if not os.path.exists(RATING_LOG_FILE):
        print("\nNo past ratings found.")
        return
    
    with open(RATING_LOG_FILE, 'r') as f:
        log_data = json.load(f)
    
    if not log_data:
        print("\nNo past ratings found.")
        return
    
    print(f"\n{'='*70}")
    print("RATING HISTORY")
    print(f"{'='*70}")
    print(f"{'#':<5} {'Ticker':<15} {'Type':<15} {'Date':<25}")
    print('-'*70)
    
    for i, entry in enumerate(reversed(log_data), 1):
        dt = datetime.fromisoformat(entry['timestamp'])
        print(f"{i:<5} {entry['ticker']:<15} {entry['rating_type']:<15} {dt.strftime('%b %d, %Y %I:%M %p'):<25}")
    
    print('='*70)
    
    choice = input("\nEnter rating number to view (or press Enter to go back): ").strip()
    
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(log_data):
            entry = list(reversed(log_data))[idx]
            display_rating(entry['ticker'], entry['rating'])
            
            export = input("\nExport this rating? (y/n): ").strip().lower()
            if export == 'y':
                export_rating(entry['ticker'], entry['rating'])
        else:
            print("Invalid selection.")


def main():
    """Main function"""
    print("="*70)
    print("AI STOCK SCREENER & RATING SYSTEM")
    print("Comprehensive Stock Evaluation Tool")
    print("="*70)
    
    api_key = get_api_key()
    
    if not api_key:
        print("\nNo API key provided. Exiting.")
        return
    
    print("\n✓ API key loaded successfully!")
    
    while True:
        print("\n" + "="*70)
        print("OPTIONS")
        print("="*70)
        print("1. Rate a specific stock (1-10 rating)")
        print("2. Screen for stocks matching criteria")
        print("3. View past ratings")
        print("4. Delete saved API key")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            ticker = input("\nEnter stock ticker to rate: ").strip()
            
            if not ticker:
                print("No ticker provided.")
                continue
            
            rating = rate_stock(ticker, api_key)
            display_rating(ticker, rating)
            
            save_rating(ticker, rating, 'individual_rating')
            print("\n✓ Rating saved to log!")
            
            export = input("\nExport to text file? (y/n): ").strip().lower()
            if export == 'y':
                export_rating(ticker, rating)
        
        elif choice == '2':
            print("\n" + "="*70)
            print("STOCK SCREENING")
            print("="*70)
            print("Describe what you're looking for in stocks.")
            print("\nExamples:")
            print("- 'Tech companies with strong moats and growing revenue'")
            print("- 'Dividend stocks with 10+ year track record'")
            print("- 'Undervalued companies in healthcare sector'")
            print("- 'Growth stocks with innovative products'")
            print("="*70)
            
            criteria = input("\nWhat criteria are you looking for?\n> ").strip()
            
            if not criteria:
                print("No criteria provided.")
                continue
            
            recommendations = screen_stocks(criteria, api_key)
            
            print(f"\n{'='*70}")
            print(f"STOCK RECOMMENDATIONS")
            print(f"Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
            print(f"{'='*70}\n")
            print(recommendations)
            print(f"\n{'='*70}")
            
            save_rating(None, recommendations, 'screening')
            print("\n✓ Recommendations saved to log!")
            
            export = input("\nExport to text file? (y/n): ").strip().lower()
            if export == 'y':
                filename = f"stock_screen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(filename, 'w') as f:
                    f.write(f"STOCK SCREENING RESULTS\n")
                    f.write(f"Criteria: {criteria}\n")
                    f.write(f"Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}\n")
                    f.write("="*70 + "\n\n")
                    f.write(recommendations)
                print(f"\n✓ Recommendations exported to: {filename}")
        
        elif choice == '3':
            view_past_ratings()
        
        elif choice == '4':
            if os.path.exists(API_KEY_FILE):
                confirm = input("\nDelete saved API key? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    os.remove(API_KEY_FILE)
                    print("\n✓ API key deleted!")
                else:
                    print("\nDeletion cancelled.")
            else:
                print("\nNo saved API key found.")
        
        elif choice == '5':
            print("\nHappy investing! 📈")
            break
        
        else:
            print("Invalid option. Please select 1-5.")


if __name__ == "__main__":
    main()
