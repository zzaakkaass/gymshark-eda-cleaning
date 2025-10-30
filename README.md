# gymshark-eda-cleaning

simple pipeline for cleaning and normalizing the Gymshark dataset. the goal is to take the raw csv files, apply business rules (drop products with no price, infer `product_type`, fill missing images) and output a clean csv ready for eda/modeling.

> this repo includes a small sample file at `data/raw/sample_gymshark.csv` so you can run it right after cloning.

---

## quickstart

```bash
git clone https://github.com/zzaakkaass/gymshark-eda-cleaning.git
cd gymshark-eda-cleaning

# create and activate venv (recommended)
python -m venv .venv
source .venv/bin/activate  # windows: .venv\Scripts\activate

# install in dev mode
pip install -e ".[dev]"

# run cleaning on the sample data
python -m gsclean run --input-path data/raw --output-path data/processed

# optional: open the streamlit viewer
streamlit run notebooks/app.py
features
read csv files from data/raw/

drop useless column (inventory_quantity)

filter out products with price <= 0

classify missing product_type based on title/tags

“greedy” filling of image_src by looking at same handle/title/type

output to data/processed/clean.csv

automated tests with pytest

cli (python -m gsclean or gsclean run ...)

simple streamlit explorer

project structure
text
Copiar código
.
├── data/
│   ├── raw/
│   │   └── sample_gymshark.csv   # sample input (committed)
│   └── processed/
│       └── README.md             # explains output
├── notebooks/
│   └── app.py                    # streamlit demo
├── src/
│   └── gsclean/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cleaning.py           # cleaning logic
│       ├── cli.py                # command line interface
│       └── io.py                 # read/write helpers
├── tests/
│   └── test_cleaning.py
├── pyproject.toml
├── .env.example
└── .gitignore
requirements
python 3.10+

pip

(optional) virtualenv

installation (dev)
bash
Copiar código
python -m venv .venv
source .venv/bin/activate  # windows: .venv\Scripts\activate
pip install -e ".[dev]"
usage (cli)
put your raw csvs under data/raw/ and run:

bash
Copiar código
gsclean run --input-path data/raw --output-path data/processed
# or
python -m gsclean run --input-path data/raw --output-path data/processed
this will generate:

text
Copiar código
data/processed/clean.csv
usage (python)
python
Copiar código
from gsclean.cleaning import clean
from gsclean.io import load_raw, save_processed

df = load_raw("data/raw")
df_clean, stats = clean(df, verbose=True)
save_processed(df_clean, "data/processed")
print(stats)
environment variables
create a .env (not tracked) based on .env.example:

bash
Copiar código
PYTHONPATH=src
this makes src/ importable during local development and testing.

streamlit demo
this project includes a simple streamlit demo to explore the cleaned data.

run:

bash
Copiar código
streamlit run notebooks/app.py
by default it will try to load:

text
Copiar código
data/processed/clean.csv
if the file does not exist, run the cleaning pipeline first:

bash
Copiar código
python -m gsclean run --input-path data/raw --output-path data/processed
requirements:

bash
Copiar código
pip install streamlit pandas
exploratory data analysis (eda)
this repo also stores some basic eda findings on top of the cleaned dataset.

1. price statistics
max price: usd 1,000.00

min price: usd 1.00

mean price: usd 27.76

most expensive item: gymshark collegiate crop tank - ink teal

price: usd 1,000.00

category: womens tank

2. expensive products analysis
products above usd 500: 12

percentage of total: 0.03%

average price of expensive items: usd 1,000.00

classification: outlier / special items

reason: only 12 products above the threshold

distribution by category:

womens tank: 12 products

conclusion: the high-price segment is concentrated in a single category, so these items should be treated as outliers in modeling.

3. top 5 categories (by product count)
mens t-shirt: 4,430 products

mens shorts: 3,323 products

womens leggings: 2,878 products

womens shorts: 2,691 products

womens sports bras: 2,506 products

these numbers help to:

detect category imbalance

decide which categories to prioritize

spot anomalies (very small categories vs very large ones)

tests
bash
Copiar código
pytest -v
notes
data folders are mostly ignored in git to keep the repo light.

a minimal sample (data/raw/sample_gymshark.csv) is provided so the pipeline can be run immediately.

streamlit is optional, but documented, so the description is not an empty promise.