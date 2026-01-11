"""Custom enrichment functions for demonstrating selection bias.

This module provides treatment effect functions that demonstrate selection bias
in observational studies. The main function selects products based on quality
score, creating selection bias for pedagogical demonstrations.
"""

import copy
from typing import Dict, List, Set

import pandas as pd


def quality_selection_boost(sales: List[Dict], **kwargs) -> List[Dict]:
    """
    Apply treatment with quality-based selection and heterogeneous effects.

    Select high quality products for treatment (mimicking business behavior
    of optimizing best content first). Effect is smaller for high quality
    products (less room to improve).

    This creates selection bias where:

    - Baseline bias > 0 (treated have higher Y^0)
    - Selection on gains < 0 (treated have smaller delta)
    - Net effect: overestimation if baseline bias dominates

    Parameters
    ----------
    sales : list of dict
        Sale transaction dictionaries.
    **kwargs : dict
        Additional parameters:

        - effect_size : float, default 0.5
            Base treatment effect magnitude.
        - enrichment_fraction : float, default 0.3
            Fraction of products to treat.
        - products_df : pandas.DataFrame
            DataFrame with product info including quality_score.

    Returns
    -------
    list of dict
        Modified sale dictionaries with treatment applied.

    Raises
    ------
    ValueError
        If products_df is not provided.
    """
    effect_size = kwargs.get("effect_size", 0.5)
    enrichment_fraction = kwargs.get("enrichment_fraction", 0.3)
    products_df = kwargs.get("products_df")

    if products_df is None:
        raise ValueError("products_df with quality_score is required")

    # Build quality lookup
    id_col = "asin" if "asin" in products_df.columns else "product_id"
    quality_map = products_df.set_index(id_col)["quality_score"].fillna(3.0).to_dict()

    # Select TOP quality products for treatment
    sorted_products = sorted(quality_map.keys(), key=lambda x: quality_map[x], reverse=True)
    n_treated = int(len(sorted_products) * enrichment_fraction)
    treated_ids = set(sorted_products[:n_treated])

    # Apply heterogeneous treatment effect
    treated_sales = []
    for sale in sales:
        sale_copy = copy.deepcopy(sale)
        product_id = sale_copy.get("product_id", sale_copy.get("asin"))

        if product_id in treated_ids:
            quality = quality_map.get(product_id, 3.0)
            # Effect decreases with quality: ~50% at q=1, ~10% at q=5
            adjusted_effect = effect_size * (1.5 - 0.1 * quality)

            original_units = sale_copy["ordered_units"]
            sale_copy["ordered_units"] = int(original_units * (1 + adjusted_effect))
            unit_price = sale_copy.get("unit_price", sale_copy.get("price"))
            sale_copy["revenue"] = round(sale_copy["ordered_units"] * unit_price, 2)

        treated_sales.append(sale_copy)

    return treated_sales


def get_treated_products_by_quality(products_df: pd.DataFrame, enrichment_fraction: float = 0.3) -> Set[str]:
    """
    Get the set of treated product IDs based on quality selection.

    Use the same selection logic as quality_selection_boost to identify
    which products would be treated (top quality products).

    Parameters
    ----------
    products_df : pandas.DataFrame
        DataFrame with product info including quality_score.
    enrichment_fraction : float, optional
        Fraction of products to treat. Default is 0.3.

    Returns
    -------
    set of str
        Product IDs in the treatment group.
    """
    id_col = "asin" if "asin" in products_df.columns else "product_id"
    quality_map = products_df.set_index(id_col)["quality_score"].fillna(3.0).to_dict()

    sorted_products = sorted(quality_map.keys(), key=lambda x: quality_map[x], reverse=True)
    n_treated = int(len(sorted_products) * enrichment_fraction)

    return set(sorted_products[:n_treated])
