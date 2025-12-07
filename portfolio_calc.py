#!/usr/bin/env python3
"""
Portfolio Allocation Calculator
Divides investment amount across specified tickers with predefined percentages
"""

def calculate_portfolio_allocation(total_amount):
    """
    Calculate allocation amounts for each ticker based on portfolio percentages
    
    Args:
        total_amount (float): Total amount to invest
        
    Returns:
        dict: Dictionary with ticker symbols and their allocated amounts
    """
    # Portfolio allocation percentages
    portfolio = {
        'ENB': 0.07,      # 7%
        'PFE': 0.07,      # 7%
        'Corweave': 0.07, # 7%
        'CEG': 0.07,      # 7%
        'TTWO': 0.07,     # 7%
        'QQQM': 0.35,     # 35%
        'BTC/ZCash': 0.30 # 30%
    }
    
    # Calculate allocations
    allocations = {}
    for ticker, percentage in portfolio.items():
        allocations[ticker] = total_amount * percentage
    
    return allocations


def display_allocations(total_amount, allocations):
    """
    Display portfolio allocations in a formatted table
    
    Args:
        total_amount (float): Total investment amount
        allocations (dict): Dictionary of ticker allocations
    """
    print("\n" + "="*60)
    print(f"PORTFOLIO ALLOCATION FOR ${total_amount:,.2f}")
    print("="*60)
    print(f"{'Ticker':<15} {'Percentage':<15} {'Amount':<15}")
    print("-"*60)
    
    total_allocated = 0
    for ticker, amount in allocations.items():
        percentage = (amount / total_amount) * 100
        print(f"{ticker:<15} {percentage:>6.1f}%{'':<8} ${amount:>12,.2f}")
        total_allocated += amount
    
    print("-"*60)
    print(f"{'TOTAL':<15} {'100.0%':<15} ${total_allocated:>12,.2f}")
    print("="*60)


def main():
    """Main function to run the portfolio calculator"""
    print("Portfolio Allocation Calculator")
    print("-" * 60)
    
    while True:
        try:
            # Get investment amount from user
            amount_input = input("\nEnter total investment amount (or 'q' to quit): $")
            
            if amount_input.lower() == 'q':
                print("\nThank you for using Portfolio Allocation Calculator!")
                break
            
            # Remove commas and convert to float
            total_amount = float(amount_input.replace(',', ''))
            
            if total_amount <= 0:
                print("Error: Please enter a positive amount.")
                continue
            
            # Calculate and display allocations
            allocations = calculate_portfolio_allocation(total_amount)
            display_allocations(total_amount, allocations)
            
        except ValueError:
            print("Error: Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n\nExiting program...")
            break


if __name__ == "__main__":
    main()
