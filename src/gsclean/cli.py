from rich import print
from typer import Typer

from .cleaning import clean
from .io import load_raw, save_processed

app = Typer(help="gsclean: limpeza e EDA do gymshark")


@app.callback()
def callback():
    pass


@app.command()
def run(input_path: str = "data/raw", output_path: str = "data/processed"):
    df = load_raw(input_path)
    df2, _stats = clean(df)
    save_processed(df2, output_path)
    print("[green]ok[/green] dados limpos e salvos.")


def main():
    app()


if __name__ == "__main__":
    main()
