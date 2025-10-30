# gymshark-eda-cleaning

simple pipeline for cleaning and normalizing the Gymshark dataset. the goal is to take the raw CSV files, apply business rules (drop products with no price, infer `product_type`, fill missing images) and output a clean CSV ready for EDA/modeling.

## features
- read CSV files from `data/raw/`
- drop useless column (`inventory_quantity`)
- filter out products with `price <= 0`
- classify missing `product_type` based on title/tags
- "greedy" filling of `image_src` by looking at same handle/title/type
- output to `data/processed/clean.csv`
- automated tests with `pytest`
- cli (`python -m gsclean` or `gsclean run ...`)

## project structure
```text
.
├── data/
│   ├── raw/          # original csvs (not versioned)
│   └── processed/    # cleaned csvs (not versioned)
├── notebooks/        # exploration and drafts
├── src/
│   └── gsclean/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cleaning.py   # cleaning logic
│       ├── cli.py        # command line interface
│       └── io.py         # read/write helpers
├── tests/
│   └── test_cleaning.py
├── pyproject.toml
├── .env.example
└── .gitignore
```

requirements
python 3.10+

pip

(optional) virtualenv
```
dev installation
python -m venv .venv
source .venv/bin/activate  # windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

usage (cli)

put your raw CSVs under data/raw/

```
run:

gsclean run --input-path data/raw --output-path data/processed


or

python -m gsclean run --input-path data/raw --output-path data/processed
```

this will generate data/processed/clean.csv.

usage (python)
```
import pandas as pd
from gsclean.cleaning import clean
from gsclean.io import load_raw, save_processed
```
```
df = load_raw("data/raw")
df_clean, stats = clean(df, verbose=True)
save_processed(df_clean, "data/processed")
print(stats)
```
tests
```
pytest -v
```

environment variables

create a .env (not tracked) based on .env.example:
```
PYTHONPATH=src
```
## streamlit demo

this project includes a simple streamlit demo to explore the cleaned data.

run:

```
streamlit run notebooks/app.py
```
or, if you prefer to point to a processed file:
```
streamlit run notebooks/app.py -- --data-path data/processed/clean.csv
```

requirements:
```
pip install streamlit pandas
```

e aí no README você coloca, sem rodeio:

## streamlit demo

```bash
streamlit run notebooks/app.py


requirements:

pip install streamlit pandas




#exploratory data analysis (eda)

this repo is also meant to keep track of basic EDA results on top of the cleaned dataset.

1. price statistics

max price: USD 1,000.00

min price: USD 1.00

mean price: USD 27.76

most expensive item: Gymshark Collegiate Crop Tank - Ink Teal

price: USD 1,000.00

category: Womens Tank

2. expensive products analysis

products above USD 500: 12

percentage of total: 0.03%

avg price of expensive items: USD 1,000.00

classification: outlier / special items

reason: only 12 products above the threshold

distribution by category:

Womens Tank: 12 products

conclusion: high-price segment is concentrated in a single category, so it should be treated as outliers in modeling.

3. top 5 categories (by product count)

Mens T-Shirt: 4,430 products

Mens Shorts: 3,323 products

Womens Leggings: 2,878 products

Womens Shorts: 2,691 products

Womens Sports Bras: 2,506 products

these numbers are useful to:

spot category imbalance

prioritize which categories to model first

detect anomalies (tiny categories vs huge ones)



first “real” project always looks messy from the inside.
