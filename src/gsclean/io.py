from pathlib import Path

import pandas as pd


def load_raw(path: str):
    path = Path(path)
    # implemente sua regra. exemplo: concatena todos csvs do diretório
    files = list(path.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"sem csv em {path.resolve()}")
    return pd.concat((pd.read_csv(f) for f in files), ignore_index=True)


def save_processed(df, path: str, name: str = "clean.csv"):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    df.to_csv(path / name, index=False)
