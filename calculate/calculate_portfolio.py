import pandas as pd
from datetime import datetime
from helpers.utils.api import get_price
from helpers.utils.constants import FILE_PATHS, LTH_YEARS

def calculate_portfolio(input_file, output_file):
    """
    Process a portfolio CSV file, fetch current prices, and calculate stats.

    Args:
        input_file (str): Path to the input CSV file containing the portfolio.
        output_file (str): Path to save the processed portfolio CSV.
    """
    # Load portfolio data
    portfolio = pd.read_csv(input_file)

    if portfolio.empty:
        print("Portfolio is empty. Check your CSV file.")
        return

    # Initialize columns
    portfolio['Type'] = portfolio['Type'].fillna('').astype(str).str.lower()
    portfolio['Liquidity'] = portfolio['Liquidity'].fillna('').astype(str).str.lower()
    portfolio['Current Price'] = 0
    portfolio['Value'] = 0
    portfolio['Gain/Loss'] = 0
    portfolio['% Gain/Loss'] = 0
    portfolio['Long-Term Hold'] = ''

    total_value = 0

    for index, row in portfolio.iterrows():
        ticker = row['Ticker']
        asset_type = row['Type']
        quantity = row['Quantity']
        cost_basis = row.get('Cost Basis', 0)
        purchase_date = row.get('Purchase Date', '')

        if pd.isna(ticker) or pd.isna(asset_type) or pd.isna(quantity):
            print(f"Skipping row {index} due to missing data: {row}")
            continue

        # Handle different asset types
        if asset_type == "cash":
            price, value, gain_loss, percentage_gain_loss = 1, quantity, 0, 0
        elif asset_type in ["401k", "hsa"]:
            price = 1
            value = price * quantity
            gain_loss = value - cost_basis
            percentage_gain_loss = (gain_loss / cost_basis) * 100 if cost_basis > 0 else 100
        else:
            price = get_price(ticker, asset_type)
            if price is None:
                print(f"Unknown asset type for {ticker}. Skipping.")
                continue
            value = price * quantity
            gain_loss = value - (cost_basis * quantity) if cost_basis > 0 else value
            percentage_gain_loss = (gain_loss / (cost_basis * quantity)) * 100 if cost_basis > 0 else 100

        total_value += value

        # Determine long-term hold status
        if not pd.isna(purchase_date):
            try:
                purchase_date_obj = datetime.strptime(str(purchase_date), "%Y-%m-%d")
                hold_duration_years = (datetime.now() - purchase_date_obj).days / 365
                long_term_hold = "Green" if hold_duration_years > LTH_YEARS else "Red"
            except ValueError:
                long_term_hold = "Invalid Date"
        else:
            long_term_hold = "No Date"

        # Update portfolio data
        portfolio.at[index, 'Current Price'] = price
        portfolio.at[index, 'Value'] = value
        portfolio.at[index, 'Gain/Loss'] = gain_loss
        portfolio.at[index, '% Gain/Loss'] = percentage_gain_loss
        portfolio.at[index, 'Long-Term Hold'] = long_term_hold

    # Save updated portfolio
    portfolio.to_csv(output_file, index=False)
    print(f"Portfolio saved to {output_file}")

if __name__ == "__main__":
    calculate_portfolio(FILE_PATHS['PORTFOLIO_INPUT'], FILE_PATHS['PORTFOLIO_OUTPUT'])