"""
Configuration for the GulfMart Retail synthetic dataset generator.

This module contains:
- Dataset size configuration
- Date range
- Geography
- Store configuration
- Channel configuration
- Product/category configuration
- Customer behavior profiles
- Pricing and margin rules
- Data-quality issue rates

The configuration is validated by validate_generation_config.py
before data generation begins.
"""

from pathlib import Path


# ============================================================
# 1. GENERAL DATASET CONFIGURATION
# ============================================================

RANDOM_SEED = 42

N_CUSTOMERS = 5_000
N_PRODUCTS = 500
N_PHYSICAL_STORES = 20

START_DATE = "2024-01-01"
END_DATE = "2025-12-31"

TARGET_FACT_ROWS = 100_000


# ============================================================
# 2. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw"
CLEANED_DATA_PATH = PROJECT_ROOT / "data" / "cleaned"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed"


# ============================================================
# 3. GEOGRAPHY CONFIGURATION
# ============================================================

REGION_CITIES = {
    "Central": ["Riyadh", "Qassim"],
    "Western": ["Jeddah", "Makkah", "Madinah"],
    "Eastern": ["Dammam", "Khobar"],
    "Northern": ["Tabuk"],
    "Southern": ["Abha"],
}


CITY_TO_REGION = {
    city: region for region, cities in REGION_CITIES.items() for city in cities
}


# ============================================================
# 4. STORE CONFIGURATION
# ============================================================

STORE_TYPE_SHARE = {"Supermarket": 0.50, "Hypermarket": 0.25, "Express": 0.25}


STORE_CHANNEL_SHARE = {"Store": 0.75, "E-commerce": 0.25}


ECOMMERCE_STORE = {
    "store_id": "ECOM01",
    "store_name": "GulfMart Online",
    "store_type": "E-commerce",
    "city": "Riyadh",
    "region": "Central",
}


# ============================================================
# 5. CUSTOMER CONFIGURATION
# ============================================================

GENDER_PROBABILITIES = {"Male": 0.52, "Female": 0.48}


AGE_GROUP_PROBABILITIES = {
    "18-24": 0.10,
    "25-34": 0.30,
    "35-44": 0.30,
    "45-54": 0.20,
    "55+": 0.10,
}


CUSTOMER_BEHAVIOR_PROBABILITIES = {
    "High Engagement": 0.10,
    "Regular": 0.30,
    "Occasional": 0.30,
    "Low Engagement": 0.20,
    "Lapsed-Prone": 0.10,
}


CHANNEL_PREFERENCE_PROBABILITIES = {
    "Store-Oriented": 0.60,
    "Digital-Oriented": 0.15,
    "Omnichannel": 0.25,
}


# ============================================================
# 6. CUSTOMER BEHAVIOR PROPENSITY
# ============================================================

PURCHASE_PROPENSITY_BASE = {
    "High Engagement": 1.80,
    "Regular": 1.20,
    "Occasional": 0.80,
    "Low Engagement": 0.45,
    "Lapsed-Prone": 0.70,
}


PURCHASE_PROPENSITY_VARIATION = (0.75, 1.25)


BASKET_FACTOR_RANGE = (0.75, 1.35)


# ============================================================
# 7. PRODUCT CATEGORY CONFIGURATION
# ============================================================

CATEGORY_CONFIG = {
    "Grocery": {
        "weight": 0.20,
        "subcategories": ["Rice", "Pasta", "Canned Food", "Cooking Essentials"],
        "price_range": (5, 80),
        "margin_range": (0.12, 0.25),
    },
    "Dairy": {
        "weight": 0.12,
        "subcategories": ["Milk", "Yogurt", "Cheese", "Butter"],
        "price_range": (4, 45),
        "margin_range": (0.15, 0.28),
    },
    "Beverages": {
        "weight": 0.13,
        "subcategories": ["Water", "Soft Drinks", "Juice", "Energy Drinks"],
        "price_range": (2, 35),
        "margin_range": (0.12, 0.30),
    },
    "Snacks": {
        "weight": 0.10,
        "subcategories": ["Chips", "Biscuits", "Chocolate", "Nuts"],
        "price_range": (3, 40),
        "margin_range": (0.20, 0.38),
    },
    "Household": {
        "weight": 0.10,
        "subcategories": ["Cleaning", "Paper Products", "Kitchen", "Laundry"],
        "price_range": (8, 120),
        "margin_range": (0.20, 0.38),
    },
    "Personal Care": {
        "weight": 0.08,
        "subcategories": ["Shampoo", "Skin Care", "Oral Care", "Body Care"],
        "price_range": (8, 150),
        "margin_range": (0.25, 0.45),
    },
    "Frozen Food": {
        "weight": 0.07,
        "subcategories": [
            "Frozen Vegetables",
            "Frozen Meat",
            "Frozen Snacks",
            "Ice Cream",
        ],
        "price_range": (8, 100),
        "margin_range": (0.18, 0.35),
    },
    "Bakery": {
        "weight": 0.07,
        "subcategories": ["Bread", "Pastries", "Cakes", "Cookies"],
        "price_range": (3, 80),
        "margin_range": (0.20, 0.40),
    },
    "Fresh Food": {
        "weight": 0.08,
        "subcategories": ["Fruits", "Vegetables", "Meat", "Chicken"],
        "price_range": (5, 180),
        "margin_range": (0.12, 0.30),
    },
    "Baby Care": {
        "weight": 0.05,
        "subcategories": ["Diapers", "Baby Food", "Baby Hygiene", "Baby Accessories"],
        "price_range": (10, 200),
        "margin_range": (0.20, 0.40),
    },
}

# ============================================================
# 7A. CUSTOMER CATEGORY AFFINITY
# ============================================================

CATEGORY_AFFINITY_VARIATION = (0.50, 1.50)

# ============================================================
# 8. STORE FORMAT BEHAVIOR
# ============================================================

STORE_FORMAT_BASKET_FACTOR = {"Supermarket": 1.00, "Hypermarket": 1.35, "Express": 0.70}


STORE_FORMAT_QUANTITY_RANGE = {
    "Supermarket": (1, 6),
    "Hypermarket": (2, 8),
    "Express": (1, 4),
}


# ============================================================
# 9. TRANSACTION CONFIGURATION
# ============================================================

TRANSACTION_LINES_RANGE = (1, 8)


QUANTITY_RANGE = (1, 8)


# ============================================================
# 10. DISCOUNT CONFIGURATION
# ============================================================

DISCOUNT_RATES = [0.00, 0.05, 0.10, 0.15, 0.20]


DISCOUNT_PROBABILITIES = [0.55, 0.20, 0.12, 0.08, 0.05]


# ============================================================
# 11. TRANSACTION TYPE CONFIGURATION
# ============================================================

TRANSACTION_TYPE_PROBABILITIES = {"Sale": 0.97, "Return": 0.03}


# ============================================================
# 12. SEASONALITY CONFIGURATION
# ============================================================

SEASONALITY_MULTIPLIERS = {
    "Ramadan": {
        "Grocery": 1.25,
        "Beverages": 1.20,
        "Fresh Food": 1.20,
        "Snacks": 1.15,
        "Bakery": 1.15,
    },
    "Eid": {"Snacks": 1.20, "Beverages": 1.15, "Personal Care": 1.20},
    "Summer": {"Beverages": 1.20, "Frozen Food": 1.15, "Household": 1.05},
    "Back-to-School": {
        "Snacks": 1.15,
        "Beverages": 1.10,
        "Household": 1.05,
        "Baby Care": 1.05,
    },
}
# ============================================================
# SEASONAL PERIODS
# ============================================================

# These are synthetic analytical windows used by the generator.
# They are intentionally fixed so the dataset is reproducible.

SEASONAL_PERIODS = [
    {"name": "Ramadan", "start": "2024-03-11", "end": "2024-04-09"},
    {"name": "Eid", "start": "2024-04-10", "end": "2024-04-12"},
    {"name": "Summer", "start": "2024-06-01", "end": "2024-08-31"},
    {"name": "Back-to-School", "start": "2024-08-18", "end": "2024-09-14"},
    {"name": "Ramadan", "start": "2025-03-01", "end": "2025-03-30"},
    {"name": "Eid", "start": "2025-03-31", "end": "2025-04-02"},
    {"name": "Summer", "start": "2025-06-01", "end": "2025-08-31"},
    {"name": "Back-to-School", "start": "2025-08-18", "end": "2025-09-14"},
]

# ============================================================
# SEASONALITY MULTIPLIERS
# ============================================================

SEASONALITY_MULTIPLIERS = {
    "Ramadan": {
        "Grocery": 1.30,
        "Dairy": 1.20,
        "Beverages": 1.25,
        "Snacks": 1.15,
        "Household": 1.10,
        "Personal Care": 1.05,
        "Frozen Food": 1.15,
        "Bakery": 1.20,
        "Fresh Food": 1.20,
        "Baby Care": 1.05,
    },
    "Eid": {
        "Grocery": 1.10,
        "Dairy": 1.05,
        "Beverages": 1.20,
        "Snacks": 1.30,
        "Household": 1.05,
        "Personal Care": 1.25,
        "Frozen Food": 1.10,
        "Bakery": 1.25,
        "Fresh Food": 1.10,
        "Baby Care": 1.05,
    },
    "Summer": {
        "Grocery": 1.00,
        "Dairy": 1.00,
        "Beverages": 1.30,
        "Snacks": 1.15,
        "Household": 1.10,
        "Personal Care": 1.05,
        "Frozen Food": 1.25,
        "Bakery": 0.95,
        "Fresh Food": 1.05,
        "Baby Care": 1.05,
    },
    "Back-to-School": {
        "Grocery": 1.05,
        "Dairy": 1.10,
        "Beverages": 1.20,
        "Snacks": 1.30,
        "Household": 1.15,
        "Personal Care": 1.05,
        "Frozen Food": 1.05,
        "Bakery": 1.10,
        "Fresh Food": 1.00,
        "Baby Care": 1.15,
    },
}


# ============================================================
# 13. DATA QUALITY ISSUE RATES
# ============================================================

DATA_QUALITY_ISSUE_RATES = {
    "missing_customer_attributes": 0.01,
    "missing_product_attributes": 0.01,
    "missing_fact_attributes": 0.0075,
    "duplicate_fact_rows": 0.005,
    "zero_negative_quantity": 0.005,
    "invalid_price": 0.004,
    "invalid_discount": 0.003,
    "orphan_customer_id": 0.0025,
    "orphan_product_id": 0.0025,
    "orphan_store_id": 0.002,
    "category_casing_inconsistency": 0.01,
    "store_type_inconsistency": 0.005,
    "invalid_future_date": 0.002,
    "transaction_before_join_date": 0.002,
    "sales_calculation_mismatch": 0.0025,
    "profit_calculation_mismatch": 0.0025,
}


# ============================================================
# 14. OUTPUT FILE NAMES
# ============================================================

OUTPUT_FILES = {
    "dim_date": "dim_date.csv",
    "dim_customer": "dim_customer.csv",
    "dim_product": "dim_product.csv",
    "dim_store": "dim_store.csv",
    "fact_sales": "fact_sales.csv",
    "customer_behavior": "customer_behavior.csv",
}
