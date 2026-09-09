"""gera as tabelas usadas no dashboard (artifact e power bi) a partir do dataset bruto.

as tabelas pequenas (os achados da analise prescritiva) sao versionadas em
powerbi/data/. a tabela produto-a-produto e grande demais pra git e vai pra
data/processed/, que ja e ignorado pelo .gitignore do projeto.

uso:
    PYTHONPATH=src python powerbi/prepare_data.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

RAW_PATH = Path("data/raw/gymshark_products.csv")
SMALL_TABLES_DIR = Path("powerbi/data")
PRODUCTS_TABLE_PATH = Path("data/processed/powerbi_products.csv")

TIER_ORDER = ["same_handle", "same_title_type", "similar_title_token", "unresolved"]
TIER_LABELS = {
    "same_handle": "1. mesmo handle",
    "same_title_type": "2. mesmo titulo+tipo",
    "similar_title_token": "3. token do titulo",
    "unresolved": "4. nao resolvido",
}


def _greedy_filler_tiered(df: pd.DataFrame) -> dict[int, str]:
    """mesma logica de gsclean.cleaning._greedy_image_filler, mas registrando
    qual das 3 camadas resolveu (ou nao) cada linha, pra alimentar o funil."""
    missing_mask = df["image_src"].isna() | (df["image_src"].astype(str).str.strip() == "")
    tier_of: dict[int, str] = {}

    for idx in df[missing_mask].index:
        current = df.loc[idx]

        if "handle" in df.columns:
            same_handle = df[(df["handle"] == current.get("handle")) & df["image_src"].notna()]
            if len(same_handle) > 0:
                df.loc[idx, "image_src"] = same_handle["image_src"].iloc[0]
                tier_of[idx] = "same_handle"
                continue

        same_title_type = df[
            (df.get("title") == current.get("title"))
            & (df.get("product_type") == current.get("product_type"))
            & df["image_src"].notna()
        ]
        if len(same_title_type) > 0:
            df.loc[idx, "image_src"] = same_title_type["image_src"].iloc[0]
            tier_of[idx] = "same_title_type"
            continue

        if isinstance(current.get("title"), str) and isinstance(current.get("product_type"), str):
            first_token = current["title"].split()[0]
            mask = (
                (df.get("product_type") == current["product_type"])
                & df["image_src"].notna()
                & df.get("title").astype(str).str.contains(first_token, na=False, regex=False)
            )
            similar = df[mask]
            if len(similar) > 0:
                df.loc[idx, "image_src"] = similar["image_src"].iloc[0]
                tier_of[idx] = "similar_title_token"
                continue

        tier_of[idx] = "unresolved"

    return tier_of


def build_image_fill_funnel(df: pd.DataFrame) -> pd.DataFrame:
    initial_missing = int(
        (df["image_src"].isna() | (df["image_src"].astype(str).str.strip() == "")).sum()
    )
    tier_of = _greedy_filler_tiered(df)
    funnel = (
        pd.Series(tier_of, name="tier")
        .value_counts()
        .reindex(TIER_ORDER, fill_value=0)
        .rename_axis("tier")
        .reset_index(name="products")
    )
    funnel["label"] = funnel["tier"].map(TIER_LABELS)
    funnel["initial_missing"] = initial_missing
    return funnel


def build_price_outliers(df: pd.DataFrame) -> pd.DataFrame:
    cols = ["handle", "title", "variant_title", "sku", "product_type", "price"]
    return df[df["price"] > 500][cols].reset_index(drop=True)


def build_category_fragmentation(df: pd.DataFrame) -> pd.DataFrame:
    pt = df["product_type"].dropna().astype(str)
    norm = pt.str.strip().str.lower()
    counts = (
        pd.DataFrame({"raw": pt, "norm": norm})
        .groupby(["norm", "raw"])
        .size()
        .reset_index(name="count")
    )
    dupe_norms = counts.groupby("norm")["raw"].nunique()
    dupe_norms = dupe_norms[dupe_norms > 1].index
    frag = counts[counts["norm"].isin(dupe_norms)]
    return frag.sort_values(["norm", "count"], ascending=[True, False]).reset_index(drop=True)


def build_category_counts(df: pd.DataFrame) -> pd.DataFrame:
    counts = df["product_type"].value_counts().reset_index()
    counts.columns = ["product_type", "count"]
    return counts


def build_products_table(df: pd.DataFrame) -> pd.DataFrame:
    cols = ["handle", "title", "product_type", "vendor", "price"]
    out = df[cols].copy()
    out["is_price_outlier"] = out["price"] > 500
    return out


def main() -> None:
    df = pd.read_csv(RAW_PATH)
    df = df[df["price"] > 0].copy()

    SMALL_TABLES_DIR.mkdir(parents=True, exist_ok=True)
    build_image_fill_funnel(df).to_csv(SMALL_TABLES_DIR / "image_fill_funnel.csv", index=False)
    build_price_outliers(df).to_csv(SMALL_TABLES_DIR / "price_outliers.csv", index=False)
    build_category_fragmentation(df).to_csv(
        SMALL_TABLES_DIR / "category_fragmentation.csv", index=False
    )
    build_category_counts(df).to_csv(SMALL_TABLES_DIR / "category_counts.csv", index=False)

    PRODUCTS_TABLE_PATH.parent.mkdir(parents=True, exist_ok=True)
    build_products_table(df).to_csv(PRODUCTS_TABLE_PATH, index=False)

    print(f"tabelas pequenas em {SMALL_TABLES_DIR}/")
    print(f"tabela completa (nao versionada) em {PRODUCTS_TABLE_PATH}")


if __name__ == "__main__":
    main()
