import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dash import Dash, html, dcc, Input, Output, State, callback_context
from helpers.utils.constants import PORTS, FUNCTIONS
from helpers.utils.helpers import parse_args, kill_port, open_browser, run_function
from helpers.utils.styling import STYLES, STYLE_CONFIG, THEMES, get_colors, set_current_theme, generate_main_content
from threading import Timer

def main():
    global current_theme, SHOW_DOLLAR

    kill_port(PORTS['PORT_MAIN'])

    app = Dash(__name__, suppress_callback_exceptions=True)

    def get_layout():
        current_theme = STYLE_CONFIG['theme']['current_theme']
        style = {
            **STYLES['DEFAULT'],
            "backgroundColor": STYLE_CONFIG['theme']['background']
        }
        return html.Div(
            style=style,
            children=[
                # Theme Dropdown Section
                html.Div(
                    [
                        html.Label("Select Theme:", style={"fontSize": "16px", "fontWeight": "bold"}),
                        dcc.Dropdown(
                            id="theme_dropdown",
                            options=[{"label": theme.title(), "value": theme} for theme in THEMES],
                            value=current_theme,
                            style={"width": "50%", "margin": "0 auto", "color": STYLE_CONFIG['theme']['color']},
                        ),
                    ],
                    style={"textAlign": "center", "marginBottom": "20px"},
                ),
                # Main Content Section (Dynamic Content)
                html.Div(
                    id="main_content",
                    style={"padding": "20px"},
                    children=generate_main_content(current_theme),
                ),
            ],
        )

    @app.callback(
        [Output("feature_flag_label", "children"), Output("feature_flag_button", "children")],
        Input("feature_flag_button", "n_clicks"),
    )
    def toggle_feature_flag(n_clicks):
        global SHOW_DOLLAR
        SHOW_DOLLAR = n_clicks % 2 == 0
        return ("Balance Visible" if SHOW_DOLLAR else "Balance Hidden",
                "Hide" if SHOW_DOLLAR else "Show")

    @app.callback(
        Output("output", "children"),
        [
            Input("run_calculate_portfolio", "n_clicks"),
            Input("visualize_portfolio", "n_clicks"),
            Input("visualize_budget", "n_clicks"),
            Input("convert_fidelity", "n_clicks"),
            Input("merge_portfolios", "n_clicks"),
        ],
        [State("calculate_portfolio_dropdown", "value"), State("theme_dropdown", "value")],
    )
    def handle_button_click(
        calc_port_click, vis_port_click, vis_budget_click, convert_click, merge_click,
        calc_port_mode, selected_theme
    ):
        triggered = callback_context.triggered
        if not triggered:
            return "No action taken yet."

        button_id = triggered[0]["prop_id"].split(".")[0]

        # Handle calculate_portfolio dropdown case
        if button_id == "run_calculate_portfolio" and calc_port_mode:
            func_entry = FUNCTIONS.get(calc_port_mode)
            if not func_entry:
                return f"Invalid mode: {calc_port_mode}"
            script_name, port = func_entry if isinstance(func_entry, tuple) else (func_entry, None)
        else:
            func_entry = FUNCTIONS.get(button_id)
            if not func_entry:
                return f"Invalid action: {button_id}"
            script_name, port = func_entry if isinstance(func_entry, tuple) else (func_entry, None)

        # Run the appropriate script
        if port:
            run_function(script_name, port, SHOW_DOLLAR, selected_theme)
        else:
            os.system(f"python3 {script_name} &")

        return f"Running: {os.path.splitext(os.path.basename(script_name))[0].replace('_', ' ').title()}"
    
    app.layout = get_layout()
    @app.callback(
        Output("theme_dropdown", "value"),
        Input("theme_dropdown", "value"),
    )
    def update_theme(selected_theme):
        if callback_context.triggered and "theme_dropdown" in callback_context.triggered[0]["prop_id"]:
            STYLE_CONFIG["theme"]["current_theme"] = selected_theme
            STYLE_CONFIG["theme"]["colors"] = get_colors(selected_theme)
        return selected_theme
    
    @app.callback(
        Output("main_content", "children"),
        Input("theme_dropdown", "value"),
    )
    def update_main_content(selected_theme):
        global current_theme
        if callback_context.triggered and "theme_dropdown" in callback_context.triggered[0]["prop_id"]:
            current_theme = selected_theme
            set_current_theme(selected_theme)
        return generate_main_content(selected_theme)

    Timer(1, open_browser, args=[PORTS['PORT_MAIN']]).start()
    app.run_server(debug=True, use_reloader=False, port=PORTS['PORT_MAIN'])


if __name__ == "__main__":
    args = parse_args()
    SHOW_DOLLAR = args.show_dollar
    set_current_theme(args.theme)
    main()