import csv
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from helpers.utils.constants import CONVERSION_CONSTANTS, FILE_PATHS
from helpers.utils.helpers import clean_numeric

def convert_fidelity(input_file, output_file):
    """
    Converts Fidelity CSV data to the required portfolio format.

    Args:
        input_file (str): Path to the input Fidelity CSV file.
        output_file (str): Path to save the converted portfolio CSV.
    """
    # Store cash adjustments for pending activity
    pending_activity_adjustments = {}
    cash_balances = {}  # To merge multiple cash rows
    portfolio_rows = []

    with open(input_file, "r") as infile:
        reader = csv.reader(infile)
        next(reader)  # Skip the header

        for row in reader:
            if len(row) < 15:  # Ensure there are enough columns
                continue

            ticker = row[2].strip()  # Column C: Symbol (Ticker)
            description = row[3].strip()  # Column D: Description
            quantity = clean_numeric(row[4])  # Column E: Quantity
            last_price = clean_numeric(row[5])  # Column F: Last Price
            current_value = clean_numeric(row[7])  # Column H: Current Value
            gain_loss = clean_numeric(row[10])  # Column K: Total Gain/Loss Dollar
            percent_gain_loss = row[11] or "0%"  # Column L: Total Gain/Loss Percent
            cost_basis = clean_numeric(row[13])  # Column N: Cost Basis Total
            account_name = row[1].strip().lower()  # Column B: Account Name
            account_id = row[0].strip()  # Column A: Account Number

            # Determine Type, Ticker, and Liquidity
            if "401k" in account_name:
                asset_type = "401k"
                ticker = description  # Use Description as the ticker for 401K
                liquidity = "low"
            elif "hsa" in account_name:
                asset_type = "hsa"
                ticker = ticker  # Use Symbol as the ticker for HSA
                liquidity = "low"
            elif any(keyword in ticker for keyword in CONVERSION_CONSTANTS['KEYWORDS']['PENDING_ACTIVITY']):
                # Store pending activity adjustments for cash
                pending_activity_adjustments[account_id] = pending_activity_adjustments.get(account_id, 0) + current_value
                continue  # Skip this row for now
            elif any(keyword in description for keyword in CONVERSION_CONSTANTS['KEYWORDS']['MONEY_MARKET']):
                asset_type = "cash"
                liquidity = "high"
            else:
                asset_type = "stock"
                liquidity = "medium"

            # Calculate Long-Term Hold (default to "No Date")
            long_term_hold = "No Date"

            # Aggregate cash balances if it's a cash row
            if asset_type == "cash":
                if account_id not in cash_balances:
                    cash_balances[account_id] = {
                        "ticker": ticker,
                        "asset_type": asset_type,
                        "quantity": 0,
                        "cost_basis": 0,
                        "liquidity": liquidity,
                        "current_value": 0,
                        "gain_loss": 0,
                        "percent_gain_loss": "0%",
                        "long_term_hold": long_term_hold
                    }
                cash_balances[account_id]["current_value"] += current_value
                continue

            # Add the processed row
            portfolio_rows.append([
                ticker, asset_type, quantity, cost_basis, None, liquidity,
                last_price, current_value, gain_loss, percent_gain_loss, long_term_hold
            ])

    # Adjust cash balances for pending activity
    for account_id, adjustment in pending_activity_adjustments.items():
        if account_id in cash_balances:
            cash_balances[account_id]["current_value"] += adjustment

    # Merge cash rows into portfolio_rows
    for cash_row in cash_balances.values():
        portfolio_rows.append([
            cash_row["ticker"], cash_row["asset_type"], cash_row["quantity"],
            cash_row["cost_basis"], None, cash_row["liquidity"],
            1, cash_row["current_value"], cash_row["gain_loss"],
            cash_row["percent_gain_loss"], cash_row["long_term_hold"]
        ])

    # Write the output
    with open(output_file, "w", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(CONVERSION_CONSTANTS['OUTPUT_HEADERS'])
        writer.writerows(portfolio_rows)

    print(f"Converted data saved to {output_file}")

if __name__ == "__main__":
    input_file = FILE_PATHS['FIDELITY_INPUT']
    output_file = FILE_PATHS['FIDELITY_OUTPUT']
    convert_fidelity(input_file, output_file)