# Financial Tracker

The Financial Tracker is a Python-based tool for managing and visualizing financial data, including portfolios, budgets, and investment performance. The tool supports data from multiple sources, processes the data, and provides analytics and visualizations.

---

## Features

1. **Portfolio Management**:
   - Calculate portfolio performance using `calculate_portfolio.py`.
   - Update portfolio prices with `update.py`.
   - Merge portfolios with `merge_portfolios.py`.

2. **Budget Analysis**:
   - Analyze income and expenses using `visualize_budget.py`.
   - Calculate budgets with `calculate_budget.py`.

3. **Data Conversions**:
   - Convert Fidelity portfolio data using `convert_fidelity.py`.

4. **Visualization**:
   - Visualize portfolio performance with `visualize_portfolio.py`.
   - Visualize budget analysis with `visualize_budget.py`.

---

## File Structure

```plaintext
├── calculate
│   ├── calculate_budget.py
│   ├── calculate_portfolio.py
│   └── update.py
├── helpers
│   ├── conversions
│   │   ├── convert_fidelity.py
│   │   ├── data
│   │   │   ├── fidelity_input.csv
│   │   │   ├── fidelity_output.csv
│   │   │   └── portfolio_output.csv
│   │   └── merge_portfolios.py
│   └── utils
│       ├── api.py
│       ├── constants.py
│       ├── helpers.py
│       └── styling.py
├── input
│   ├── api_key.md
│   ├── crypto.csv
│   ├── income_expenses.csv
│   └── portfolio_input.csv
├── main.py
└── visualize
    ├── visualize_budget.py
    └── visualize_portfolio.py
```

---

## Prerequisites

- Python 3.10+
- Required Python libraries (`requirements.txt`)
- Alpha Vantage API key (`input/api_key.md`)

---

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/financial-tracker.git
    cd financial-tracker
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Add your API key to `input/api_key.md`:

    ```plaintext
    ALPHA_VANTAGE_API_KEY=your_api_key_here
    ```

---

## Input File Formats

### 1. Portfolio Input File (`portfolio_input.csv`)
| Ticker | Type   | Quantity | Cost Basis | Purchase Date | Liquidity |
|--------|--------|----------|------------|---------------|-----------|
| AAPL   | stock  | 10       | 150        | 2023-01-01    | high      |

### 2. Income/Expenses File (`income_expenses.csv`)
| Date       | Category      | Type       | Amount |
|------------|---------------|------------|--------|
| 2023-01-01 | Groceries     | Expense    | 200.00 |
| 2023-01-02 | Salary        | Income     | 5000.00 |
| 2023-01-03 | Rent          | Expense    | 1500.00 |

### 3. Fidelity Input File (`fidelity_input.csv`)
| Ticker         | Description                 | Quantity | Cost Basis | Type   |
|----------------|-----------------------------|----------|------------|--------|
| AAPL           | Apple Inc                   | 5        | 300.00     | stock  |

### This file can be obtained directly from Fidelity's website.

1. Navigate to either the "Positions" tab or the "Activity & Orders" tab.
2. Click the download icon in the top right corner and select .csv as the file format.
3. Save the file locally and re-name as fidelity_input.csv in the helpers/conversions/data/ directory.

---

## Usage

### 1. Main Application

```bash
python3 main.py
```

This launches the Dash application for managing and visualizing your financial data.

### 2. Individual Scripts

#### Calculate Portfolio
```bash
python3 calculate/calculate_portfolio.py
```

#### Update Portfolio Prices
```bash
python3 calculate/update.py
```

#### Convert Fidelity Data
```bash
python3 helpers/conversions/convert_fidelity.py
```

#### Merge Portfolios
```bash
python3 helpers/conversions/merge_portfolios.py
```

#### Visualize Portfolio
```bash
python3 visualize/visualize_portfolio.py
```

#### Visualize Budget
```bash
python3 visualize/visualize_budget.py
```

---

## Requirements

Install `requirements.txt` with:
```bash
pip install -r requirements.txt
```

---

## Contributions

Feel free to contribute by opening issues or submitting pull requests.

