import argparse, os, psutil, webbrowser

def parse_args():
    """
    Parse command-line arguments for visualization options.
    
    Returns:
        argparse.Namespace: Parsed arguments with `show_dollar` and `theme`.
    """
    parser = argparse.ArgumentParser(description="Visualize Portfolio")
    parser.add_argument("--show-dollar", type=lambda x: x.lower() in ["true", "1", "yes"], default=True, help="Show dollar values")
    parser.add_argument("--theme", type=str, default="blue", help="Theme to use")
    return parser.parse_args()

def clean_numeric(value):
    """Cleans and converts a numeric string by removing $ and commas."""
    try:
        return float(value.replace("$", "").replace(",", ""))
    except ValueError:
        return 0

def kill_port(port):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            for conn in proc.connections(kind='inet'):
                if conn.laddr.port == port:
                    proc.kill()
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            continue

def open_browser(port):
    webbrowser.open_new(f"http://127.0.0.1:{port}")

def run_function(script_name, port, show_dollar, theme):
    kill_port(port)
    os.system(f"python3 {script_name} --show-dollar {str(show_dollar).lower()} --theme {theme} &")