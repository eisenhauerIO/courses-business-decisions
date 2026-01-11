"""Support functions for the Catalog AI notebook."""


def print_product_details(products, label=None):
    """Print formatted product details from LLM-generated output."""
    if label:
        print(f"\n{'=' * 70}")
        print(f"{label.upper()}")
        print(f"{'=' * 70}")
    for _, row in products.iterrows():
        print(f"\n  Title: {row['title']}")
        print(f"  Brand: {row['brand']}")
        print(f"  Description: {row['description']}")
