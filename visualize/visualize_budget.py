import os, sys
import pandas as pd
import plotly.express as px, plotly.graph_objects as go
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dash import Dash, dcc, html
from helpers.utils.constants import FILE_PATHS, PORTS
from helpers.utils.helpers import parse_args, kill_port, open_browser
from helpers.utils.styling import (
    COLOR_SCHEMES,
    STYLES,
    configure_pie_traces,
    set_current_theme
)
from threading import Timer

def visualize_budget(data_file):
    """
    Generate and display budget visualizations using Dash.

    Args:
        data_file (str): Path to the CSV file containing budget data.
    """
    # Free the port for the budget visualization
    kill_port(PORTS['PORT_BUDGET'])

    # Load budget data
    data = pd.read_csv(data_file)

    # Split data into income and expenses
    income_data = data[data["Category"].str.lower() == "income"].sort_values(by="Amount", ascending=False)
    expenses_data = data[data["Category"].str.lower() == "expenses"].sort_values(by="Amount", ascending=False)

    if income_data.empty or expenses_data.empty:
        raise ValueError("Both income and expenses data must be present.")

    # Calculate totals and savings
    total_income = income_data["Amount"].sum()
    total_expenses = expenses_data["Amount"].sum()
    savings = total_income - total_expenses

    # Prepare data for the Sankey diagram
    nodes = []
    links = {"source": [], "target": [], "value": [], "color": []}
    combined_colors = COLOR_SCHEMES['PIE'] * ((len(income_data) + len(expenses_data)) // len(COLOR_SCHEMES['PIE']) + 1)

    def add_node(label):
        """Add a unique node to the Sankey diagram."""
        if label not in nodes:
            nodes.append(label)
        return nodes.index(label)

    # Add income nodes to the Sankey diagram
    for i, row in income_data.iterrows():
        source_idx = add_node(row["Source"])
        budget_idx = add_node("Budget")
        links["source"].append(source_idx)
        links["target"].append(budget_idx)
        links["value"].append(row["Amount"])
        links["color"].append(combined_colors[i])

    # Add expense nodes to the Sankey diagram
    for i, row in expenses_data.iterrows():
        budget_idx = add_node("Budget")
        expense_idx = add_node(row["Source"])
        links["source"].append(budget_idx)
        links["target"].append(expense_idx)
        links["value"].append(row["Amount"])
        links["color"].append(combined_colors[len(income_data) + i])

    # Add savings node if savings are positive
    if savings > 0:
        budget_idx = add_node("Budget")
        savings_idx = add_node("Savings")
        links["source"].append(budget_idx)
        links["target"].append(savings_idx)
        links["value"].append(savings)
        links["color"].append("#197")  # Custom savings color

    # Create Dash app
    app = Dash(__name__)

    # Layout for the Dash app
    app.layout = html.Div(style=STYLES['DEFAULT'], children=[
        # Title Section
        html.H1("Budget Visualization", style=STYLES['H1']),
        html.Hr(style=STYLES['DIVIDER']),

        # Cash Flow Section (Sankey Diagram)
        html.Div(style={
            "backgroundColor": STYLES['TABLE']["backgroundColor"],
            "padding": "30px",
            "borderRadius": "15px",
            "marginBottom": "30px",
            "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.25)"
        }, children=[
            html.H2("Cash Flow", style=STYLES['H2']),
            dcc.Graph(
                figure=go.Figure(go.Sankey(
                    node=dict(
                        pad=25,
                        thickness=30,
                        line=dict(color=STYLES['DEFAULT']["color"], width=0.5),
                        label=nodes,
                        color=STYLES['DEFAULT']["color"]
                    ),
                    link=dict(
                        source=links["source"],
                        target=links["target"],
                        value=links["value"],
                        color=links["color"],
                        hovertemplate="<b>%{source.label} → %{target.label}</b><br>"
                                      f"{'Amount: $%{value:,.2f}' if SHOW_DOLLAR else 'Percentage: %{value:.1f}%'}<extra></extra>"
                    )
                )).update_layout(
                    margin=dict(l=50, r=50, t=50, b=50),
                    height=600,
                    paper_bgcolor=STYLES['TABLE']["backgroundColor"],
                )
            )
        ]),
        html.Hr(style=STYLES['DIVIDER']),

        # Expense Breakdown Section (Pie Chart)
        html.Div(style={
            "backgroundColor": STYLES['TABLE']["backgroundColor"],
            "padding": "20px",
            "borderRadius": "10px",
            "marginBottom": "20px"
        }, children=[
            html.H2("Expense Breakdown", style=STYLES['H2']),
            dcc.Graph(
                figure=configure_pie_traces(
                    px.pie(
                        expenses_data,
                        values="Amount",
                        names="Source",
                    ).update_layout(
                        paper_bgcolor=STYLES['TABLE']["backgroundColor"],
                        font=dict(
                            family=STYLES['DEFAULT']["fontFamily"],
                            color=STYLES['DEFAULT']["color"]
                        )
                    ),
                    expenses_data["Amount"],
                    show_dollar=SHOW_DOLLAR
                )
            )
        ]),
        html.Hr(style=STYLES['DIVIDER']),

        # Income and Expense Table Section
        html.Div(style={
            "backgroundColor": STYLES['TABLE']["backgroundColor"],
            "padding": "20px",
            "borderRadius": "10px",
            "marginBottom": "20px"
        }, children=[
            html.H2("Details", style=STYLES['H2']),

            # Income Table
            html.Table([
                # Income Section Header
                html.Tr([
                    html.Th("Income", colSpan=2, style=STYLES['TABLE_SECTION_TITLE'])
                ]),
                # Income Table Header
                html.Tr([
                    html.Th("Source", style={**STYLES['TABLE_HEADER'], "width": "50%"}),
                    html.Th("Amount", style={**STYLES['TABLE_HEADER'], "width": "50%"})
                ]),
                # Income Table Rows
                *[
                    html.Tr([
                        html.Td(row["Source"], style={**STYLES['TABLE_ROW'], "width": "50%"}),
                        html.Td(
                            f"${row['Amount']:,.2f}" if SHOW_DOLLAR else f"{(row['Amount'] / total_income) * 100:.1f}%",
                            style={**STYLES['TABLE_ROW'], "width": "50%"}
                        )
                    ])
                    for _, row in income_data.iterrows()
                ]
            ], style=STYLES['TABLE']),

            html.Hr(style=STYLES['DIVIDER']),

            # Expenses Table
            html.Table([
                # Expenses Section Header
                html.Tr([
                    html.Th("Expenses", colSpan=2, style=STYLES['TABLE_SECTION_TITLE'])
                ]),
                # Expenses Table Header
                html.Tr([
                    html.Th("Source", style={**STYLES['TABLE_HEADER'], "width": "50%"}),
                    html.Th("Amount", style={**STYLES['TABLE_HEADER'], "width": "50%"})
                ]),
                # Expenses Table Rows
                *[
                    html.Tr([
                        html.Td(row["Source"], style={**STYLES['TABLE_ROW'], "width": "50%"}),
                        html.Td(
                            f"${row['Amount']:,.2f}" if SHOW_DOLLAR else f"{(row['Amount'] / total_expenses) * 100:.1f}%",
                            style={**STYLES['TABLE_ROW'], "width": "50%"}
                        )
                    ])
                    for _, row in expenses_data.iterrows()
                ]
            ], style=STYLES['TABLE'])
        ])
    ])

    # Automatically open the app in the browser
    Timer(1, open_browser, args=[PORTS['PORT_BUDGET']]).start()

    # Run the Dash server
    app.run_server(debug=True, use_reloader=False, port=PORTS['PORT_BUDGET'])


if __name__ == "__main__":
    args = parse_args()
    SHOW_DOLLAR = args.show_dollar
    set_current_theme(args.theme)
    visualize_budget(FILE_PATHS['CASH_FLOW'])