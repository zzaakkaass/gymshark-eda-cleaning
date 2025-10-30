import pandas as pd
import pytest
from gsclean.cleaning import clean

# dataframe fictício pra simular o dataset bruto
@pytest.fixture
def raw_df():
    return pd.DataFrame({
        "title": ["Gymshark Beanie", "Basic Cap", "Running Socks", "Random Bag", "Broken Item"],
        "tags": ["winter", "sport", "footwear", "travel", "misc"],
        "product_type": [None, None, None, None, None],
        "price": [39.99, 19.99, 12.5, 45.0, 0],
        "image_src": [None, "img_cap.jpg", None, None, "img_broken.jpg"],
        "handle": ["beanie-001", "cap-001", "sock-001", "bag-001", "broken-001"],
        "inventory_quantity": [10, 20, 15, 30, 5],
    })

def test_clean_filters_and_classifies(raw_df):
    df_clean, stats = clean(raw_df, verbose=False)

    # deve remover itens com preço <= 0
    assert all(df_clean["price"] > 0), "deveria filtrar produtos com preço inválido"

    # a coluna inventory_quantity deve sumir
    assert "inventory_quantity" not in df_clean.columns

    # deve preencher product_type com base em regras
    assert df_clean["product_type"].notna().all(), "há product_type não preenchido"

    # deve retornar dict de métricas coerente
    assert "rows_out" in stats and stats["rows_out"] == len(df_clean)

def test_clean_handles_missing_columns_gracefully(raw_df):
    df = raw_df.drop(columns=["image_src"])
    df_clean, stats = clean(df, verbose=False, fill_images=False)
    assert "rows_out" in stats
    assert isinstance(df_clean, pd.DataFrame)

def test_clean_empty_df():
    empty = pd.DataFrame(columns=["price"])
    out, stats = clean(empty, verbose=False)
    assert out.empty
    assert stats["rows_out"] == 0
