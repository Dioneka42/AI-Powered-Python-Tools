#!/usr/bin/env python3
"""
Investment Tracker with Historical Data
Tracks deposits, allocations, and calculates averages over time
"""

import json
import os
from datetime import datetime, timedelta
from statistics import mean

# Portfolio allocation percentages
PORTFOLIO = {
    'ENB': 0.07,
    'PFE': 0.07,
    'Corweave': 0.07,
    'CEG': 0.07,
    'TTWO': 0.07,
    'QQQM': 0.35,
    'BTC/ZCash': 0.30
}

DATA_FILE = 'investment_log.json'


def load_data():
    """Load investment history from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {'deposits': []}


def save_data(data):
    """Save investment history to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def add_deposit(amount):
    """Add a new deposit to the log"""
    data = load_data()
    
    # Calculate allocations
    allocations = {ticker: amount * pct for ticker, pct in PORTFOLIO.items()}
    
    # Create deposit entry
    deposit = {
        'timestamp': datetime.now().isoformat(),
        'amount': amount,
        'allocations': allocations
    }
    
    data['deposits'].append(deposit)
    save_data(data)
    
    return deposit


def display_deposit(deposit):
    """Display a single deposit with allocations"""
    dt = datetime.fromisoformat(deposit['timestamp'])
    print(f"\n{'='*70}")
    print(f"DEPOSIT RECORDED: {dt.strftime('%B %d, %Y at %I:%M %p')}")
    print(f"{'='*70}")
    print(f"Total Amount: ${deposit['amount']:,.2f}\n")
    print(f"{'Ticker':<15} {'Percentage':<15} {'Amount':<15}")
    print('-'*70)
    
    for ticker, amount in deposit['allocations'].items():
        percentage = (amount / deposit['amount']) * 100
        print(f"{ticker:<15} {percentage:>6.1f}%{'':<8} ${amount:>12,.2f}")
    
    print('='*70)


def get_deposits_in_range(deposits, days):
    """Get deposits within the last N days"""
    cutoff = datetime.now() - timedelta(days=days)
    return [d for d in deposits if datetime.fromisoformat(d['timestamp']) >= cutoff]


def calculate_averages(deposits):
    """Calculate average deposits for different time periods"""
    if not deposits:
        return None
    
    now = datetime.now()
    
    # Get deposits for each period
    week_deposits = get_deposits_in_range(deposits, 7)
    month_deposits = get_deposits_in_range(deposits, 30)
    six_month_deposits = get_deposits_in_range(deposits, 180)
    year_deposits = get_deposits_in_range(deposits, 365)
    
    averages = {
        'week': mean([d['amount'] for d in week_deposits]) if week_deposits else 0,
        'month': mean([d['amount'] for d in month_deposits]) if month_deposits else 0,
        'six_months': mean([d['amount'] for d in six_month_deposits]) if six_month_deposits else 0,
        'year': mean([d['amount'] for d in year_deposits]) if year_deposits else 0,
        'all_time': mean([d['amount'] for d in deposits])
    }
    
    counts = {
        'week': len(week_deposits),
        'month': len(month_deposits),
        'six_months': len(six_month_deposits),
        'year': len(year_deposits),
        'all_time': len(deposits)
    }
    
    return averages, counts


def display_statistics():
    """Display investment statistics and averages"""
    data = load_data()
    deposits = data['deposits']
    
    if not deposits:
        print("\nNo deposits recorded yet.")
        return
    
    total_invested = sum(d['amount'] for d in deposits)
    averages, counts = calculate_averages(deposits)
    
    print(f"\n{'='*70}")
    print("INVESTMENT STATISTICS")
    print(f"{'='*70}")
    print(f"Total Deposits: {len(deposits)}")
    print(f"Total Invested: ${total_invested:,.2f}")
    print(f"\n{'Period':<20} {'Avg Deposit':<20} {'# Deposits':<15}")
    print('-'*70)
    print(f"{'Last 7 Days':<20} ${averages['week']:>12,.2f}       {counts['week']}")
    print(f"{'Last 30 Days':<20} ${averages['month']:>12,.2f}       {counts['month']}")
    print(f"{'Last 6 Months':<20} ${averages['six_months']:>12,.2f}       {counts['six_months']}")
    print(f"{'Last Year':<20} ${averages['year']:>12,.2f}       {counts['year']}")
    print(f"{'All Time':<20} ${averages['all_time']:>12,.2f}       {counts['all_time']}")
    print('='*70)
    
    # Portfolio totals
    print(f"\nTOTAL PORTFOLIO ALLOCATION")
    print('-'*70)
    portfolio_totals = {ticker: 0 for ticker in PORTFOLIO.keys()}
    for deposit in deposits:
        for ticker, amount in deposit['allocations'].items():
            portfolio_totals[ticker] += amount
    
    print(f"{'Ticker':<15} {'Total Invested':<15}")
    print('-'*70)
    for ticker, total in portfolio_totals.items():
        print(f"{ticker:<15} ${total:>12,.2f}")
    print('='*70)


def view_history(limit=10):
    """View recent deposit history"""
    data = load_data()
    deposits = data['deposits']
    
    if not deposits:
        print("\nNo deposits recorded yet.")
        return
    
    print(f"\n{'='*70}")
    print(f"RECENT DEPOSITS (Last {min(limit, len(deposits))})")
    print(f"{'='*70}")
    print(f"{'Date & Time':<25} {'Amount':<15}")
    print('-'*70)
    
    for deposit in reversed(deposits[-limit:]):
        dt = datetime.fromisoformat(deposit['timestamp'])
        print(f"{dt.strftime('%b %d, %Y %I:%M %p'):<25} ${deposit['amount']:>12,.2f}")
    
    print('='*70)


def reset_data():
    """Reset all investment data"""
    print("\n" + "!"*70)
    print("WARNING: This will delete ALL your investment data!")
    print("!"*70)
    confirm = input("\nAre you sure? Type 'YES' to confirm: ").strip()
    
    if confirm == 'YES':
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        print("\n✓ All data has been reset successfully!")
    else:
        print("\nReset cancelled.")


def delete_last_deposit():
    """Delete the most recent deposit"""
    data = load_data()
    
    if not data['deposits']:
        print("\nNo deposits to delete.")
        return
    
    # Show the last deposit
    last_deposit = data['deposits'][-1]
    dt = datetime.fromisoformat(last_deposit['timestamp'])
    
    print("\n" + "="*70)
    print("MOST RECENT DEPOSIT:")
    print("="*70)
    print(f"Date: {dt.strftime('%B %d, %Y at %I:%M %p')}")
    print(f"Amount: ${last_deposit['amount']:,.2f}")
    print("="*70)
    
    confirm = input("\nDelete this deposit? Type 'YES' to confirm: ").strip()
    
    if confirm == 'YES':
        data['deposits'].pop()
        save_data(data)
        print("\n✓ Last deposit deleted successfully!")
    else:
        print("\nDeletion cancelled.")


def main():
    """Main function"""
    print("="*70)
    print("INVESTMENT TRACKER")
    print("="*70)
    
    while True:
        print("\nOptions:")
        print("1. Add new deposit")
        print("2. View statistics & averages")
        print("3. View deposit history")
        print("4. Delete last deposit")
        print("5. Reset all data")
        print("6. Exit")
        
        choice = input("\nSelect an option (1-6): ").strip()
        
        if choice == '1':
            try:
                amount_input = input("\nEnter deposit amount: $").replace(',', '')
                amount = float(amount_input)
                
                if amount <= 0:
                    print("Error: Please enter a positive amount.")
                    continue
                
                deposit = add_deposit(amount)
                display_deposit(deposit)
                print("\n✓ Deposit logged successfully!")
                
            except ValueError:
                print("Error: Please enter a valid number.")
        
        elif choice == '2':
            display_statistics()
        
        elif choice == '3':
            try:
                limit = input("\nHow many recent deposits to show? (default 10): ").strip()
                limit = int(limit) if limit else 10
                view_history(limit)
            except ValueError:
                view_history(10)
        
        elif choice == '4':
            delete_last_deposit()
        
        elif choice == '5':
            reset_data()
        
        elif choice == '6':
            print("\nThank you for using Investment Tracker!")
            break
        
        else:
            print("Invalid option. Please select 1-6.")


if __name__ == "__main__":
    main()
