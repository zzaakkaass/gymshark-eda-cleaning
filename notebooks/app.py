from pathlib import Path

import pandas as pd
import streamlit as st

st.title("gymshark data explorer")

data_path = st.sidebar.text_input(
    "data path",
    "data/processed/clean.csv",
    help="run the cleaning pipeline first: `python -m gsclean run`",
)

path = Path(data_path)

if path.exists():
    df = pd.read_csv(path)
    st.success(f"loaded {len(df)} rows from {data_path}")

    st.subheader("preview")
    st.dataframe(df.head(50))

    if "product_type" in df.columns:
        st.subheader("top categories")
        st.bar_chart(df["product_type"].value_counts().head(10))
    else:
        st.warning("column `product_type` not found in the dataset.")
else:
    st.warning(f"file not found {data_path}")
    st.info(
        "run the cleaning pipeline first: `python -m gsclean run --input-path data/raw --output-path data/processed`"
    )
