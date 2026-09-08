
# Data Dictionary — Retail Customer RFM Analytics

## Project

**GulfMart Retail — Customer RFM Analytics**

This document describes the structure and business meaning of the data used in the customer analytics project.

> This is an initial data dictionary. Column-level definitions, data types, quality issues, and treatment decisions will be updated after data profiling.

---

# 1. Fact Sales

### Table: `fact_sales`

**Grain:** One transaction line.

| Column               | Expected Type    | Business Definition                                  | Notes                                                   |
| -------------------- | ---------------- | ---------------------------------------------------- | ------------------------------------------------------- |
| `transaction_id`   | String / Integer | Unique identifier for a customer transaction         | Frequency should count distinct qualifying transactions |
| `transaction_date` | Date / DateTime  | Date and time of the transaction                     | Used for recency and time analysis                      |
| `customer_id`      | String / Integer | Identifier of the customer who made the purchase     | Required for customer-level analysis                    |
| `product_id`       | String / Integer | Identifier of the purchased product                  | Links sales to product dimension                        |
| `store_id`         | String / Integer | Identifier of the store/channel location             | Links sales to store dimension                          |
| `quantity`         | Numeric          | Number of units purchased                            | Must be validated for invalid/negative values           |
| `unit_price`       | Numeric          | Selling price per unit before applicable adjustments | Must be validated                                       |
| `discount_amount`  | Numeric          | Discount applied to the transaction line             | Treatment will depend on business rules                 |
| `net_sales`        | Numeric          | Revenue after applicable discounts                   | Primary revenue measure                                 |
| `cost`             | Numeric          | Cost associated with the sold products               | Used for profitability analysis                         |
| `gross_profit`     | Numeric          | Net sales minus applicable cost                      | Used to distinguish revenue from profitability          |
| `channel`          | String           | Sales channel such as store or e-commerce            | Used for channel behavior analysis                      |

---

# 2. Customer Dimension

### Table: `dim_customer`

**Grain:** One row per customer.

| Column                 | Expected Type    | Business Definition                                              |
| ---------------------- | ---------------- | ---------------------------------------------------------------- |
| `customer_id`        | String / Integer | Unique customer identifier                                       |
| `customer_name`      | String           | Customer display name or anonymized identifier                   |
| `gender`             | String           | Customer gender where available                                  |
| `age_group`          | String           | Customer age band                                                |
| `city`               | String           | Customer city                                                    |
| `region`             | String           | Customer geographic region                                       |
| `customer_join_date` | Date             | Date the customer joined the retailer/loyalty program            |
| `customer_type`      | String           | Customer classification such as new or returning where available |

---

# 3. Product Dimension

### Table: `dim_product`

**Grain:** One row per product.

| Column           | Expected Type    | Business Definition             |
| ---------------- | ---------------- | ------------------------------- |
| `product_id`   | String / Integer | Unique product identifier       |
| `product_name` | String           | Product name                    |
| `category`     | String           | Product category                |
| `subcategory`  | String           | Product subcategory             |
| `brand`        | String           | Product brand                   |
| `unit_cost`    | Numeric          | Product cost per unit           |
| `unit_price`   | Numeric          | Standard selling price per unit |

---

# 4. Store Dimension

### Table: `dim_store`

**Grain:** One row per store.

| Column         | Expected Type    | Business Definition                                       |
| -------------- | ---------------- | --------------------------------------------------------- |
| `store_id`   | String / Integer | Unique store identifier                                   |
| `store_name` | String           | Store name                                                |
| `store_type` | String           | Store format such as supermarket, hypermarket, or express |
| `city`       | String           | Store city                                                |
| `region`     | String           | Store geographic region                                   |

---

# 5. Date Dimension

### Table: `dim_date`

**Grain:** One row per calendar date.

| Column          | Expected Type    | Business Definition |
| --------------- | ---------------- | ------------------- |
| `date`        | Date             | Calendar date       |
| `year`        | Integer          | Calendar year       |
| `quarter`     | Integer / String | Calendar quarter    |
| `month`       | Integer          | Month number        |
| `month_name`  | String           | Month name          |
| `week`        | Integer          | Week number         |
| `day_of_week` | String / Integer | Day of the week     |

---

# 6. Customer Analytics Fields

Customer-level analytical fields will be created during the project rather than treated as raw source fields.

Potential fields include:

| Field                  | Definition                                                |
| ---------------------- | --------------------------------------------------------- |
| `recency`            | Days since the customer's most recent qualifying purchase |
| `frequency`          | Number of distinct qualifying transactions                |
| `monetary`           | Customer monetary value from qualifying transactions      |
| `r_score`            | Recency score from 1–5                                   |
| `f_score`            | Frequency score from 1–5                                 |
| `m_score`            | Monetary score from 1–5                                  |
| `rfm_score`          | Combined RFM score                                        |
| `customer_segment`   | Business segment derived from RFM behavior                |
| `risk_level`         | Customer retention/risk classification                    |
| `recommended_action` | Suggested business action for the customer                |

---

# 7. Data Quality Notes

The following will be investigated during profiling:

* Missing values
* Duplicate records
* Duplicate transaction IDs
* Invalid dates
* Negative quantities
* Zero quantities
* Invalid prices
* Invalid sales values
* Negative sales
* Missing customer IDs
* Missing product IDs
* Missing store IDs
* Orphan foreign keys
* Inconsistent categories
* Duplicate customers
* Unexpected data types
* Return/refund transactions
* Cancelled transactions
* Zero-value transactions

Final findings and treatment decisions will be added after data profiling.

---

# 8. RFM Methodology

The project will define the following:

### Recency

Number of days between the customer's last qualifying purchase and the RFM analysis date.

### Frequency

Number of distinct qualifying transactions made by the customer.

### Monetary

Monetary value generated by qualifying transactions.

### Analysis Date

Initial methodology:

`Maximum valid transaction date + 1 day`

The final methodology will be documented after reviewing the actual transaction data and business rules.

---

# 9. Data Dictionary Status

**Status:** Initial version

The dictionary will be updated after:

1. Data profiling
2. Data cleaning
3. Data validation
4. RFM methodology confirmation
5. Final analytical model creation
