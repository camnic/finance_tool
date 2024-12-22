SHOW_DOLLAR = True
LTH_YEARS = 2

PORTS = {
    'PORT_MAIN': 8050,
    'PORT_PORTFOLIO': 8051,
    'PORT_BUDGET': 8052,
    'PORT_API': 8053,
    'PORT_ALT': 8054
}

FUNCTIONS = {
    "calculate_portfolio_new": ("calculate/calculate_portfolio.py", PORTS['PORT_API']),
    "calculate_portfolio_update": ("calculate/update.py", PORTS['PORT_API']),
    "visualize_portfolio": ("visualize/visualize_portfolio.py", PORTS['PORT_PORTFOLIO']),
    "visualize_budget": ("visualize/visualize_budget.py", PORTS['PORT_BUDGET']),
    "convert_fidelity": ("helpers/conversions/convert_fidelity.py", PORTS['PORT_ALT']),
    "merge_portfolios": ("helpers/conversions/merge_portfolios.py", PORTS['PORT_ALT'])
}

FILE_PATHS = {
    "PORTFOLIO_INPUT": "input/portfolio_input.csv",
    "PORTFOLIO_OUTPUT": "helpers/conversions/data/portfolio_output.csv",
    "CASH_FLOW": "input/income_expenses.csv",
    "FIDELITY_INPUT": "helpers/conversions/data/fidelity_input.csv",
    "FIDELITY_OUTPUT": "helpers/conversions/data/fidelity_output.csv",
    "CRYPTO": "input/crypto.csv",
}

CONVERSION_CONSTANTS = {
    "OUTPUT_HEADERS": [
        "Ticker", "Type", "Quantity", "Cost Basis", "Purchase Date", "Liquidity",
        "Current Price", "Value", "Gain/Loss", "% Gain/Loss", "Long-Term Hold"
    ],
    "KEYWORDS": {
        "MONEY_MARKET": ["HELD IN MONEY MARKET"],
        "PENDING_ACTIVITY": ["Pending Activity"]
    }
}