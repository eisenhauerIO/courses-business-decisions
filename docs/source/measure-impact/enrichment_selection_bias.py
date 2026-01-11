"""Custom enrichment function that introduces selection bias.

This module provides a treatment effect function that selects products based on
their baseline performance rather than randomly. This creates selection bias
for demonstrating why naive comparisons fail in observational studies.
"""

import copy
from collections import defaultdict
from datetime import datetime
from typing import Dict, List


def selection_bias_boost(sales: List[Dict], **kwargs) -> List[Dict]:
    """
    Treatment effect with BIASED selection: top performers get treated.

    Unlike combined_boost (random selection), this selects products with
    highest baseline revenue - mimicking real business behavior where
    companies optimize their best sellers first.

    This creates SELECTION BIAS: E[Y^0|D=1] > E[Y^0|D=0]

    Args:
        sales: List of sale transaction dictionaries
        **kwargs: Parameters including:
            - effect_size: Treatment effect magnitude (default: 0.5 for 50% boost)
            - ramp_days: Number of days for ramp-up period (default: 0)
            - enrichment_fraction: Fraction of products to treat (default: 0.3)
            - enrichment_start: Start date of treatment (default: "2024-11-15")
            - seed: Random seed for reproducibility (default: 42)

    Returns:
        List of modified sale dictionaries with treatment applied to top performers
    """
    effect_size = kwargs.get("effect_size", 0.5)
    ramp_days = kwargs.get("ramp_days", 0)
    enrichment_fraction = kwargs.get("enrichment_fraction", 0.3)
    enrichment_start = kwargs.get("enrichment_start", "2024-11-15")

    start_date = datetime.strptime(enrichment_start, "%Y-%m-%d")

    # Step 1: Calculate baseline revenue per product (pre-treatment period)
    baseline_revenue = defaultdict(float)
    for sale in sales:
        sale_date = datetime.strptime(sale["date"], "%Y-%m-%d")
        if sale_date < start_date:
            product_id = sale.get("product_id", sale.get("asin"))
            baseline_revenue[product_id] += sale.get("revenue", 0)

    # Step 2: Rank products by baseline performance and select TOP performers
    sorted_products = sorted(
        baseline_revenue.keys(), key=lambda x: baseline_revenue[x], reverse=True
    )
    n_treated = int(len(sorted_products) * enrichment_fraction)
    treated_product_ids = set(sorted_products[:n_treated])

    # Step 3: Apply treatment effect to selected products post-treatment
    treated_sales = []
    for sale in sales:
        sale_copy = copy.deepcopy(sale)
        product_id = sale_copy.get("product_id", sale_copy.get("asin"))
        sale_date = datetime.strptime(sale_copy["date"], "%Y-%m-%d")

        # Apply boost if product is in treatment group and date is after start
        if product_id in treated_product_ids and sale_date >= start_date:
            days_since_start = (sale_date - start_date).days

            # Handle ramp-up period
            if ramp_days <= 0:
                ramp_factor = 1.0
            else:
                ramp_factor = min(1.0, days_since_start / ramp_days)

            adjusted_effect = effect_size * ramp_factor

            # Boost ordered units and recalculate revenue
            original_quantity = sale_copy["ordered_units"]
            sale_copy["ordered_units"] = int(original_quantity * (1 + adjusted_effect))
            unit_price = sale_copy.get("unit_price", sale_copy.get("price"))
            sale_copy["revenue"] = round(sale_copy["ordered_units"] * unit_price, 2)

        treated_sales.append(sale_copy)

    return treated_sales


def get_treated_products(sales: List[Dict], **kwargs) -> set:
    """
    Helper function to get the set of treated product IDs.

    Uses the same selection logic as selection_bias_boost to identify
    which products would be treated.

    Args:
        sales: List of sale transaction dictionaries
        **kwargs: Same parameters as selection_bias_boost

    Returns:
        Set of product IDs that are in the treatment group
    """
    enrichment_fraction = kwargs.get("enrichment_fraction", 0.3)
    enrichment_start = kwargs.get("enrichment_start", "2024-11-15")

    start_date = datetime.strptime(enrichment_start, "%Y-%m-%d")

    # Calculate baseline revenue per product
    baseline_revenue = defaultdict(float)
    for sale in sales:
        sale_date = datetime.strptime(sale["date"], "%Y-%m-%d")
        if sale_date < start_date:
            product_id = sale.get("product_id", sale.get("asin"))
            baseline_revenue[product_id] += sale.get("revenue", 0)

    # Select top performers
    sorted_products = sorted(
        baseline_revenue.keys(), key=lambda x: baseline_revenue[x], reverse=True
    )
    n_treated = int(len(sorted_products) * enrichment_fraction)

    return set(sorted_products[:n_treated])
