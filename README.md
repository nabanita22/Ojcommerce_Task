# Ojcommerce_Task
This is a takehome task given by Ojcommerce

# Customer's data:

*About the data*


========================================
        CUSTOMER TABLE SUMMARY
========================================
  Total Customers   : 25000
  Signup Date Range : 2022-07-03 → 2024-07-01
  Cities            : 12
  States            : 11
  Segments          : ['Budget', 'Premium', 'Value']
  Duplicates        : 0
  Missing Values    : False
========================================


1. 2022 data starts from July — partial year, not comparable full-year
2. 2024 data ends at July — dataset likely extracted mid-2024
3. Only 2023 is a complete year — use as primary baseline
4. For YoY comparisons, use Jul-Dec window (common across 2022 & 2023)
5. 2024 July shows only 25 signups — likely data cutoff mid-month

*Business Insight*

- H1 (Jan-Jun): Signups grew +2.17% from 2023 → 2024 → accelerating growth
- H2 (Jul-Dec): Signups grew +1.24% from 2022 → 2023 → steady growth
- Overall trend: Customer acquisition is consistently growing year over year
- 2024 July shows only 25 signups — data likely cut off mid-July 2024


*Customer Segment Distribution by City (2023)*

Overall Segment Mix:

The platform skews towards Budget (40.7%) and Value (39.6%) segments, with Premium customers making up only 19.7% of the total base — meaning QuickKart is primarily a value-driven marketplace.

Key Findings:
1. Chandigarh leads in Premium concentration (21.4%)
Despite being a smaller city with only 369 customers, it has the highest share of Premium customers — suggesting strong purchasing power relative to its size. A high-value but underleveraged market.

2. Bangalore is the Premium capital in absolute numbers
Highest Premium % (20.8%) among large cities AND the most Premium customers in raw count (354) — making it the most attractive city for premium seller onboarding and targeted campaigns.

3. Mumbai and Delhi are volume leaders but Premium-laggards
Mumbai (2,274) and Delhi (1,957) have the largest customer bases but below-average Premium % (19.4% and 19.5%) — large markets with room to upsell Value customers into Premium.

4. Kolkata and Chennai are the weakest Premium markets
Both sit at the bottom with 18.9–19.0% Premium share — may indicate price-sensitive markets where discounting drives acquisition.

5. Kochi and Pune are small but consistent
Mid-tier cities with average Premium concentration — stable but not priority markets for premium growth strategy.

*Segment Growth Trends*

H1 (Jan–Jun): 2023 vs 2024
Budget (+2.47%) and Value (+3.29%) segments are growing steadily
Premium is slightly declining (-0.65%) — losing high-value customers in the first half of 2024 is a concern

H2 (Jul–Dec): 2022 vs 2023
All segments grew slowly and uniformly (~1–1.5%)
Premium grew the least (+0.58%) — consistent with H1 trend

*QuickKart is moving downmarket — Budget and Value customers are growing while Premium is stagnating or declining. If this trend continues, it will pressure GMV and take-rate since Premium customers typically spend more per order.*


#PRODUCT DATA:

*about the data*


========================================
        PRODUCT TABLE SUMMARY
========================================
  Total Products    : 3000
  Categories        : 5
  Sub Categories    : 21
  Duplicates        : 0
  Missing Values    : False
========================================

1. QuickKart is primarily an Electronics + Fashion marketplace — these two categories alone make up 54% of all products (by quantity).

2. Subcategory distribution is remarkably balanced within each category (by quantity)
        Every subcategory sits between 19–29% within its category
        No single subcategory is being over or under stocked

3. by price distribution:

        Electronics avg:    ₹38,000 - ₹41,000
        Home & Kitchen avg: ₹12,000 - ₹13,000
        Fashion avg:        ₹3,800 - ₹4,300
        Books avg:          ₹1,500 - ₹1,600
        Grocery avg:        ₹987 - ₹1,079

Electronics products are ~25x more expensive than Grocery — meaning even a small drop in Electronics orders will massively impact GMV

4. Smartphones have the highest mean (₹41,482) — single highest GMV driver across all subcategories

5. Electronics — Extremely High Volatility
        Range : ₹79,011  (₹827 → ₹79,838)
        Std Dev: ₹22,911

        Smartphones (min ₹827), Laptops (min ₹900) and Audio (min ₹1,072) have the highest price floors in the entire catalogue — making them the potential GMV backbone, subject to order volumes from the orders table.