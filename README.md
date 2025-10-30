# gymshark-eda-cleaning

pipeline simples de limpeza e normalização do dataset da gymshark. o objetivo é pegar os csvs brutos, aplicar regras de negócio (tirar produtos sem preço, inferir `product_type`, preencher imagem faltando) e gerar um csv limpo pra usar em eda/modelagem.

## features
- leitura de csvs a partir de `data/raw/`
- remoção de coluna inútil (`inventory_quantity`)
- filtragem de produtos com `price <= 0`
- classificação de `product_type` faltante com base em título/tags
- preenchimento "ganancioso" de `image_src` procurando no mesmo handle/título/tipo
- saída em `data/processed/clean.csv`
- testes automatizados com `pytest`
- cli (`python -m gsclean` ou `gsclean run ...`)

## estrutura do projeto
```text
.
├── data/
│   ├── raw/          # csvs originais (não vão pro git)
│   └── processed/    # csvs já limpos (não vão pro git)
├── notebooks/        # exploração e rascunhos
├── src/
│   └── gsclean/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cleaning.py   # lógica de limpeza
│       ├── cli.py        # linha de comando
│       └── io.py         # leitura/escrita
├── tests/
│   └── test_cleaning.py
├── pyproject.toml
├── .env.example
└── .gitignore
```
requisitos

python 3.10+

pip

(opcional) virtualenv

instalação em dev:

```
python -m venv .venv
source .venv/bin/activate  # windows: .venv\Scripts\activate
pip install -e ".[dev]"
```
usando pela linha de comando

coloque seus csvs brutos em data/raw/

```rode:

gsclean run --input-path data/raw --output-path data/processed


ou

python -m gsclean run --input-path data/raw --output-path data/processed
```

isso vai gerar data/processed/clean.csv.

usando em código
```
import pandas as pd
from gsclean.cleaning import clean
from gsclean.io import load_raw, save_processed

df = load_raw("data/raw")
df_clean, stats = clean(df, verbose=True)
save_processed(df_clean, "data/processed")
print(stats)

testes
pytest -v
```
variáveis de ambiente

crie um .env (que não vai pro git) baseado em .env.example:

```
PYTHONPATH=src
```

o primeiro projeto que eu tento fazer ser mais "real", ficou bagunçado, mas gostei aonde cheguei.
