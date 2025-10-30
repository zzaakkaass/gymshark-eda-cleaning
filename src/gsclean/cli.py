from typer import Typer
from rich import print
from .cleaning import clean
from .io import load_raw, save_processed

app = Typer(help="gsclean: limpeza e EDA do gymshark")

@app.command()
def run(input_path: str = "data/raw", output_path: str = "data/processed"):
    df = load_raw(input_path)
    df2 = clean(df)
    save_processed(df2, output_path)
    print("[green]ok[/green] dados limpos e salvos.")

def main():
    app()

if __name__ == "__main__":
    main()
