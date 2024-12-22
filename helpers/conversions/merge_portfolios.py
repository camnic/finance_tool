import os, sys
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from helpers.utils.constants import FILE_PATHS

def merge_portfolios(file1, file2, output_file):
    """
    Merges two portfolio files into a single portfolio file.

    Args:
        file1 (str): Path to the first portfolio CSV file.
        file2 (str): Path to the second portfolio CSV file.
        output_file (str): Path to save the merged portfolio CSV file.
    """
    # Load the two portfolios
    portfolio1 = pd.read_csv(file1)
    portfolio2 = pd.read_csv(file2)

    # Merge the portfolios
    merged_portfolio = pd.concat([portfolio1, portfolio2], ignore_index=True)

    # Save the merged portfolio to the output file
    merged_portfolio.to_csv(output_file, index=False)
    print(f"Merged portfolio saved to {output_file}")


if __name__ == "__main__":
    merge_portfolios(FILE_PATHS['FIDELITY_OUTPUT'], FILE_PATHS['CRYPTO'], FILE_PATHS['PORTFOLIO_OUTPUT'])
