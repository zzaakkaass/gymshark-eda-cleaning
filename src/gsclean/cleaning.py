# cleaning.py
from __future__ import annotations

import pandas as pd

CLASSIFICATION_RULES: dict[str, str] = {
    "beanie": "Accessories - Headwear",
    "cap": "Accessories - Headwear",
    "sock": "Accessories - Footwear",
    "bag": "Accessories - Bags",
}


def _quick_classify(title: str, tags: str) -> str:
    text = f"{title or ''} {tags or ''}".lower()
    for keyword, category in CLASSIFICATION_RULES.items():
        if keyword in text:
            return category
    return "Accessories"


def _greedy_image_filler(df: pd.DataFrame) -> int:
    """tenta preencher image_src usando: mesmo handle > mesmo título+tipo > primeiro token do título dentro do mesmo tipo."""
    if "image_src" not in df.columns:
        return 0

    missing_mask = df["image_src"].isna() | (df["image_src"].astype(str).str.strip() == "")
    filled = 0

    for idx in df[missing_mask].index:
        current = df.loc[idx]

        if "handle" in df.columns:
            same_handle = df[(df["handle"] == current.get("handle")) & df["image_src"].notna()]
            if len(same_handle) > 0:
                df.loc[idx, "image_src"] = same_handle["image_src"].iloc[0]
                filled += 1
                continue

        same_title_type = df[
            (df.get("title") == current.get("title"))
            & (df.get("product_type") == current.get("product_type"))
            & df["image_src"].notna()
        ]
        if len(same_title_type) > 0:
            df.loc[idx, "image_src"] = same_title_type["image_src"].iloc[0]
            filled += 1
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
                filled += 1
                continue

    return filled


def clean(
    df: pd.DataFrame,
    *,
    drop_col: str = "inventory_quantity",
    min_price: float = 0.0,
    classify_missing: bool = True,
    fill_images: bool = True,
    verbose: bool = True,
) -> tuple[pd.DataFrame, dict[str, int]]:
    required = ["price"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"coluna obrigatória ausente: {col}")

    out = df.copy()

    out["price"] = pd.to_numeric(out["price"], errors="coerce")

    if drop_col in out.columns:
        out = out.drop(columns=[drop_col])

    before = len(out)
    out = out[out["price"].fillna(-1) > min_price]
    after_price = len(out)

    for c in ["title", "tags", "product_type", "image_src"]:
        if c in out.columns:
            out[c] = out[c].astype("string")

    classified = 0
    if classify_missing and "product_type" in out.columns:
        missing_mask = out["product_type"].isna() | (out["product_type"].str.strip() == "")
        if "title" in out.columns and "tags" in out.columns:
            out.loc[missing_mask, "product_type"] = out[missing_mask].apply(
                lambda row: _quick_classify(row.get("title", ""), row.get("tags", "")), axis=1
            )
            classified = int(missing_mask.sum() - out["product_type"].isna().sum())

    filled_images = 0
    if fill_images and "image_src" in out.columns:
        filled_images = _greedy_image_filler(out)

    metrics = {
        "rows_in": int(before),
        "rows_after_price_filter": int(after_price),
        "product_type_filled": int(classified),
        "image_src_filled": int(filled_images),
        "rows_out": len(out),
    }

    if verbose:
        print(f"after initial cleaning: {after_price} products")
        if "product_type" in out.columns:
            print(
                f"products without product_type after classification: "
                f"{int(out['product_type'].isna().sum())}"
            )
        if "image_src" in out.columns:
            missing_img = int(
                out["image_src"].isna().sum()
                + (out["image_src"].astype(str).str.strip() == "").sum()
            )
            print(f"images still missing: {missing_img}")

    return out, metrics
