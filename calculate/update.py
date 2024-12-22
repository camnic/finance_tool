import os, sys
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from helpers.utils.api import get_price
from helpers.utils.constants import FILE_PATHS

def update_portfolio_prices(input_file):
    """
    Updates the current prices of assets in the portfolio file without changing its structure.

    Args:
        input_file (str): Path to the portfolio CSV file to be updated.
    """
    portfolio = pd.read_csv(input_file)

    if portfolio.empty:
        print("Portfolio is empty. Check your CSV file.")
        return

    total_value = 0

    for index, row in portfolio.iterrows():
        ticker = row['Ticker']
        asset_type = row['Type']
        quantity = row['Quantity']
        cost_basis = row.get('Cost Basis', 0)

        # Fetch updated price
        if asset_type == "cash":
            price, value, gain_loss, percentage_gain_loss = 1, quantity, 0, 0
        elif asset_type in ["401k", "hsa"]:
            price = 1
            value = price * quantity
            gain_loss = value - cost_basis
            percentage_gain_loss = (gain_loss / cost_basis) * 100 if cost_basis > 0 else 100
        else:
            # For dynamic assets
            price = get_price(ticker, asset_type)
            if price is None:
                print(f"Could not fetch price for {ticker} ({asset_type}). Retaining existing price.")
                price = row.get('Current Price', 0)  # Retain existing price if fetch fails

            value = price * quantity
            gain_loss = value - (cost_basis * quantity) if cost_basis > 0 else value
            percentage_gain_loss = (gain_loss / (cost_basis * quantity)) * 100 if cost_basis > 0 else 0

        # Update the portfolio row
        portfolio.at[index, 'Current Price'] = price
        portfolio.at[index, 'Value'] = value
        portfolio.at[index, 'Gain/Loss'] = gain_loss
        portfolio.at[index, '% Gain/Loss'] = percentage_gain_loss

        total_value += value

    # Save the updated portfolio back to the same file
    portfolio.to_csv(input_file, index=False)
    print(f"Updated portfolio saved to {input_file}")
    print(f"Total portfolio value: ${total_value:,.2f}")

if __name__ == "__main__":
    update_portfolio_prices(FILE_PATHS['PORTFOLIO_OUTPUT'])
