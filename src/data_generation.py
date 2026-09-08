"""
Synthetic GulfMart Retail dataset generator.

This module:
1. Validates generation configuration.
2. Creates the random number generator.
3. Generates dimension tables.
4. Generates customer behavior.
5. Generates transaction-level data.
6. Injects controlled data-quality issues.
7. Saves raw data.

Business rules and generation parameters are stored separately
in data_generation_config.py.
"""

from datetime import timedelta

import numpy as np
import pandas as pd

from data_generation_config import (
    RANDOM_SEED,
    CATEGORY_CONFIG,
    SEASONAL_PERIODS,
    SEASONALITY_MULTIPLIERS,
    N_CUSTOMERS,
    N_PRODUCTS,
    N_PHYSICAL_STORES,
    START_DATE,
    END_DATE,
    RAW_DATA_PATH,
    REGION_CITIES,
    CITY_TO_REGION,
    GENDER_PROBABILITIES,
    AGE_GROUP_PROBABILITIES,
    CATEGORY_CONFIG,
    CATEGORY_AFFINITY_VARIATION,
    STORE_TYPE_SHARE,
    STORE_FORMAT_BASKET_FACTOR,
    STORE_FORMAT_QUANTITY_RANGE,
    CUSTOMER_BEHAVIOR_PROBABILITIES,
    CHANNEL_PREFERENCE_PROBABILITIES,
    PURCHASE_PROPENSITY_BASE,
    PURCHASE_PROPENSITY_VARIATION,
    BASKET_FACTOR_RANGE,
)

from validate_generation_config import validate_config


# ============================================================
# 1. RANDOM NUMBER GENERATOR
# ============================================================

rng = np.random.default_rng(RANDOM_SEED)


# ============================================================
# 2. HELPER FUNCTIONS
# ============================================================


def weighted_choice(options, probabilities, size=1):
    """
    Select values using weighted probabilities.
    """

    return rng.choice(options, size=size, p=probabilities)


# ============================================================
# 3. DATE DIMENSION
# ============================================================


def generate_dim_date():

    dates = pd.date_range(start=START_DATE, end=END_DATE, freq="D")

    df = pd.DataFrame({"date": dates})

    df["year"] = df["date"].dt.year
    df["quarter"] = "Q" + df["date"].dt.quarter.astype(str)
    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.month_name()
    df["week"] = df["date"].dt.isocalendar().week.astype(int)
    df["day_of_week"] = df["date"].dt.day_name()

    return df


# ============================================================
# 4. CUSTOMER DIMENSION
# ============================================================


def generate_dim_customer():

    customer_ids = [f"C{i:05d}" for i in range(1, N_CUSTOMERS + 1)]

    genders = weighted_choice(
        list(GENDER_PROBABILITIES.keys()),
        list(GENDER_PROBABILITIES.values()),
        size=N_CUSTOMERS,
    )

    age_groups = weighted_choice(
        list(AGE_GROUP_PROBABILITIES.keys()),
        list(AGE_GROUP_PROBABILITIES.values()),
        size=N_CUSTOMERS,
    )

    regions = weighted_choice(
        list(REGION_CITIES.keys()), [0.35, 0.15, 0.20, 0.15, 0.15], size=N_CUSTOMERS
    )

    cities = [rng.choice(REGION_CITIES[region]) for region in regions]

    start_days = pd.Timestamp(START_DATE).value // 86_400_000_000_000

    end_days = pd.Timestamp(END_DATE).value // 86_400_000_000_000

    join_dates = pd.to_datetime(
        rng.integers(start_days, end_days + 1, size=N_CUSTOMERS), unit="D"
    )

    df = pd.DataFrame(
        {
            "customer_id": customer_ids,
            "customer_name": [f"Customer_{i:05d}" for i in range(1, N_CUSTOMERS + 1)],
            "gender": genders,
            "age_group": age_groups,
            "city": cities,
            "region": regions,
            "customer_join_date": join_dates,
        }
    )

    return df


# ============================================================
# 5. PRODUCT DIMENSION
# ============================================================


def generate_dim_product():

    categories = list(CATEGORY_CONFIG.keys())

    category_weights = [CATEGORY_CONFIG[category]["weight"] for category in categories]

    product_categories = weighted_choice(categories, category_weights, size=N_PRODUCTS)

    records = []

    for i, category in enumerate(product_categories, start=1):
        config = CATEGORY_CONFIG[category]

        subcategory = rng.choice(config["subcategories"])

        min_price, max_price = config["price_range"]

        unit_price = round(rng.uniform(min_price, max_price), 2)

        min_margin, max_margin = config["margin_range"]

        margin = rng.uniform(min_margin, max_margin)

        unit_cost = round(unit_price * (1 - margin), 2)

        records.append(
            {
                "product_id": f"P{i:04d}",
                "product_name": f"{subcategory}_Product_{i:04d}",
                "category": category,
                "subcategory": subcategory,
                "brand": f"Brand_{rng.integers(1, 31):02d}",
                "unit_cost": unit_cost,
                "unit_price": unit_price,
            }
        )

    return pd.DataFrame(records)


# ============================================================
# 6. STORE DIMENSION
# ============================================================


def generate_dim_store():

    store_records = []

    store_type_counts = {"Supermarket": 10, "Hypermarket": 5, "Express": 5}

    store_types = []

    for store_type, count in store_type_counts.items():
        store_types.extend([store_type] * count)

    physical_cities = [
        rng.choice(list(CITY_TO_REGION.keys())) for _ in range(N_PHYSICAL_STORES)
    ]

    for i in range(N_PHYSICAL_STORES):
        city = physical_cities[i]

        region = CITY_TO_REGION[city]

        store_type = store_types[i]

        store_records.append(
            {
                "store_id": f"S{i + 1:03d}",
                "store_name": f"GulfMart {store_type} {i + 1:02d}",
                "store_type": store_type,
                "city": city,
                "region": region,
            }
        )

    store_records.append(
        {
            "store_id": "ECOM01",
            "store_name": "GulfMart Online",
            "store_type": "E-commerce",
            "city": "Riyadh",
            "region": "Central",
        }
    )

    return pd.DataFrame(store_records)


# ============================================================
# 7. CUSTOMER BEHAVIOR
# ============================================================


def generate_customer_behavior(dim_customer):

    behavior_profile = weighted_choice(
        list(CUSTOMER_BEHAVIOR_PROBABILITIES.keys()),
        list(CUSTOMER_BEHAVIOR_PROBABILITIES.values()),
        size=len(dim_customer),
    )

    channel_preference = weighted_choice(
        list(CHANNEL_PREFERENCE_PROBABILITIES.keys()),
        list(CHANNEL_PREFERENCE_PROBABILITIES.values()),
        size=len(dim_customer),
    )

    purchase_propensity = np.array(
        [PURCHASE_PROPENSITY_BASE[profile] for profile in behavior_profile]
    )

    purchase_propensity *= rng.uniform(
        PURCHASE_PROPENSITY_VARIATION[0],
        PURCHASE_PROPENSITY_VARIATION[1],
        size=len(dim_customer),
    )

    basket_factor = rng.uniform(
        BASKET_FACTOR_RANGE[0], BASKET_FACTOR_RANGE[1], size=len(dim_customer)
    )

    return pd.DataFrame(
        {
            "customer_id": dim_customer["customer_id"],
            "behavior_profile": behavior_profile,
            "channel_preference": channel_preference,
            "purchase_propensity": purchase_propensity,
            "basket_factor": basket_factor,
        }
    )


# ============================================================
# 8. CUSTOMER CATEGORY AFFINITY
# ============================================================
# %%
def generate_customer_category_affinity(dim_customer):
    """
    Generate customer-specific preferences across product
    categories.

    Each customer starts with the overall category weights
    defined in CATEGORY_CONFIG. Random variation is then
    applied to create realistic customer-level differences.

    Final category probabilities for each customer sum to 1.
    """

    categories = list(CATEGORY_CONFIG.keys())

    base_weights = np.array(
        [CATEGORY_CONFIG[category]["weight"] for category in categories]
    )

    min_variation, max_variation = CATEGORY_AFFINITY_VARIATION

    records = []

    for customer_id in dim_customer["customer_id"]:
        # ----------------------------------------------------
        # Create customer-specific variation
        # ----------------------------------------------------

        variation = rng.uniform(min_variation, max_variation, size=len(categories))

        # ----------------------------------------------------
        # Apply variation to the overall category weights
        # ----------------------------------------------------

        customer_weights = base_weights * variation

        # ----------------------------------------------------
        # Normalize so probabilities sum to 1
        # ----------------------------------------------------

        customer_probabilities = customer_weights / customer_weights.sum()

        record = {"customer_id": customer_id}

        for category, probability in zip(categories, customer_probabilities):
            record[category] = probability

        records.append(record)

    return pd.DataFrame(records)


def get_seasonality_period(transaction_date):
    """
    Return the seasonal period for a transaction date.

    Possible results:
        Ramadan
        Eid
        Summer
        Back-to-School
        Normal
    """

    transaction_date = pd.Timestamp(transaction_date)

    for period in SEASONAL_PERIODS:
        start_date = pd.Timestamp(period["start"])
        end_date = pd.Timestamp(period["end"])

        if start_date <= transaction_date <= end_date:
            return period["name"]

    return "Normal"


def get_seasonality_multiplier(transaction_date, category):
    """
    Return the seasonal multiplier for a category.

    Normal periods use a multiplier of 1.0.
    """

    season = get_seasonality_period(transaction_date)

    if season == "Normal":
        return 1.0

    return SEASONALITY_MULTIPLIERS[season].get(category, 1.0)


def generate_category_probabilities(
    customer_id, transaction_date, customer_category_affinity
):
    """
    Generate final category probabilities for one customer
    on a specific transaction date.

    Final probability is influenced by:

    1. Customer-specific category affinity
    2. Seasonal category multiplier

    Returns
    -------
    dict
        Category -> final probability
    """

    # --------------------------------------------------------
    # Get the customer's affinity record
    # --------------------------------------------------------

    customer_row = customer_category_affinity[
        customer_category_affinity["customer_id"] == customer_id
    ]

    if customer_row.empty:
        raise ValueError(
            f"Customer {customer_id} not found in customer_category_affinity."
        )

    customer_row = customer_row.iloc[0]

    # --------------------------------------------------------
    # Get category names
    # --------------------------------------------------------

    categories = list(CATEGORY_CONFIG.keys())

    # --------------------------------------------------------
    # Calculate seasonally adjusted weights
    # --------------------------------------------------------

    adjusted_weights = {}

    for category in categories:
        customer_affinity = customer_row[category]

        seasonality_multiplier = get_seasonality_multiplier(transaction_date, category)

        adjusted_weights[category] = customer_affinity * seasonality_multiplier

    # --------------------------------------------------------
    # Convert weights into probabilities
    # --------------------------------------------------------

    total_weight = sum(adjusted_weights.values())

    if total_weight <= 0:
        raise ValueError("Total category weight must be greater than zero.")

    category_probabilities = {
        category: weight / total_weight for category, weight in adjusted_weights.items()
    }

    return category_probabilities


# ============================================================
# 9. MAIN GENERATION PIPELINE
# ============================================================


def main():

    # --------------------------------------------------------
    # Validate configuration BEFORE generation
    # --------------------------------------------------------

    validate_config()

    print("\nStarting GulfMart dataset generation...")

    # --------------------------------------------------------
    # Generate dimensions
    # --------------------------------------------------------

    dim_date = generate_dim_date()

    dim_customer = generate_dim_customer()

    dim_product = generate_dim_product()

    dim_store = generate_dim_store()

    # --------------------------------------------------------
    # Generate customer behavior
    # --------------------------------------------------------

    customer_behavior = generate_customer_behavior(dim_customer)

    # --------------------------------------------------------
    # Generate customer category affinity
    # --------------------------------------------------------
    customer_category_affinity = generate_customer_category_affinity(dim_customer)

    # --------------------------------------------------------
    # Temporary checkpoint
    # --------------------------------------------------------

    print("\nGeneration checkpoint:")
    print(f"dim_date: {len(dim_date):,}")
    print(f"dim_customer: {len(dim_customer):,}")
    print(f"dim_product: {len(dim_product):,}")
    print(f"dim_store: {len(dim_store):,}")
    print(f"customer_behavior: {len(customer_behavior):,}")

    print("\nDimension generation completed.")

    # Transaction generation will be added next.
    print(customer_behavior["behavior_profile"].value_counts())
    print()
    print(customer_behavior["channel_preference"].value_counts())
    print(f"customer_category_affinity: {len(customer_category_affinity):,}")

    categories = list(CATEGORY_CONFIG.keys())
    category_probability_sum = customer_category_affinity[categories].sum(axis=1)

    print("Minimum:", category_probability_sum.min())

    print("Maximum:", category_probability_sum.max())
    print(customer_category_affinity.head().T)
    print(customer_category_affinity[categories].std().sort_values(ascending=False))

    print("\nSeasonality test:")

    test_dates = [
        "2024-01-15",
        "2024-03-20",
        "2024-04-11",
        "2024-07-15",
        "2024-09-01",
        "2025-03-15",
        "2025-04-01",
        "2025-07-15",
    ]

    for test_date in test_dates:
        season = get_seasonality_period(test_date)

        beverage_multiplier = get_seasonality_multiplier(test_date, "Beverages")

        grocery_multiplier = get_seasonality_multiplier(test_date, "Grocery")

        print(
            f"{test_date} | "
            f"Season: {season:<15} | "
            f"Beverages: {beverage_multiplier:.2f} | "
            f"Grocery: {grocery_multiplier:.2f}"
        )

    normal_multiplier = get_seasonality_multiplier("2024-01-15", "Beverages")

    assert normal_multiplier == 1.0

    print("\nNormal-period validation: PASS")

    print("\nCategory probability tests:")

    test_customer_id = dim_customer["customer_id"].iloc[0]

    test_dates = [
        "2024-01-15",  # Normal
        "2024-03-20",  # Ramadan
        "2024-04-11",  # Eid
        "2024-07-15",  # Summer
    ]

    for test_date in test_dates:
        probabilities = generate_category_probabilities(
            test_customer_id, test_date, customer_category_affinity
        )

    probability_sum = sum(probabilities.values())

    print(f"\nDate: {test_date}")

    print(f"Customer: {test_customer_id}")

    print(f"Probability sum: {probability_sum:.12f}")

    print("Top categories:")

    top_categories = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)[:5]

    for category, probability in top_categories:
        print(f"  {category:<15} {probability:.4f}")
    assert abs(probability_sum - 1.0) < 1e-10

    assert all(probability >= 0 for probability in probabilities.values())

    assert set(probabilities.keys()) == set(CATEGORY_CONFIG.keys())
    normal_probabilities = generate_category_probabilities(
        test_customer_id, "2024-01-15", customer_category_affinity
    )

    ramadan_probabilities = generate_category_probabilities(
        test_customer_id, "2024-03-20", customer_category_affinity
    )

    if normal_probabilities != ramadan_probabilities:
        print("\nSeasonality effect validation: PASS")
    else:
        raise AssertionError("Seasonality did not change category probabilities.")

    customer_1 = dim_customer["customer_id"].iloc[0]
    customer_2 = dim_customer["customer_id"].iloc[1]

    probabilities_1 = generate_category_probabilities(
        customer_1, "2024-01-15", customer_category_affinity
    )

    probabilities_2 = generate_category_probabilities(
        customer_2, "2024-01-15", customer_category_affinity
    )

    if probabilities_1 != probabilities_2:
        print("Customer affinity validation: PASS")
    else:
        raise AssertionError(
            "Different customers have identical category probabilities."
        )


if __name__ == "__main__":
    main()

# %%
