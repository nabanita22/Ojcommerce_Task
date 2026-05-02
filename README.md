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


# SELLER DATA

*About the data*

========================================
        SELLER TABLE SUMMARY
========================================
  Total Sellers     : 400
  number of Cities  : 12
  Duplicates        : 0
  Missing Values    : False
========================================


1. Mumbai (19.75%), Delhi (16%) and Bangalore (13%) together host ~49% of all sellers — a logistics disruption or policy change in any of these 3 cities could impact nearly half the platform's supply side, posing a significant GMV concentration risk.


2. Seller Quality Distribution by City
      Lucknow is the surprise best performer.

      Chennai - 1 in 3 sellers in Chennai is poorly rated — highest poor seller concentration on the platform.

      Kochi - is a double risk, High poor seller % AND lowest best seller % among all cities — worst seller quality market overall

      Bangalore - 3rd largest seller base but lowest best seller % among top 3 cities.

      Kolkata &  Ahmedabad - Low poor seller concentration + high best seller % ,most reliable supply markets despite being mid-size


# ORDERS DATA

<in orders status what does it mean by shipped ? are those orders lost?>

1. H2 Order Volume (Jul-Dec): 2024 vs 2025

   Order volume dipped slightly by -1.47% (496 orders) in H2 2025 vs H2 2024 — the platform is not growing, it's marginally shrinking.

2. YOY Order Volumn Analysis:

2024 (Jul-Dec) 

October was the peak (5,791) — festive season boost
November was the worst month (5,504) — sharp post-festive drop

2025 (Jan-Dec) 

February was the lowest (5,163) — typical post-holiday slowdown
October again peaked (5,722) — festive pattern repeating
Overall trend is flat — no real growth through the year

H2 Comparison (2024 vs 2025) 

Both years follow the same pattern — dip in August/September, peak in October
2025 is slightly below 2024 in most months
November and December 2025 are noticeably weaker than 2024.

3. Cancellation Rate (7.3% - 8.8%)

Range is very tight — cancellations are consistent, not spiking
Highest: October 2024 (8.79%) — post festive season impulse orders being cancelled
Lowest: August 2025 (7.33%) — most stable month
No alarming upward trend — but stubbornly stuck around 8%

4. Return Rate (4.5% - 5.3%)

Even tighter range than cancellations
December months tend to have slightly higher returns (5.21% in 2024, gift returns?)
June 2025 highest at 5.27%
Flat trend — not improving, not worsening

5. Cancellation and return rates are flat and persistent — not a crisis yet, but losing ~13% of orders every single month is a silent GMV drain that compounds over time. 

6. payment mode vs cancellation rate & return rate
Highest cancellation (8.20%) + highest return rate (5.16%)  though Payment method has negligible impact on cancellation and return rates .

7. Fast delivery eligibility is completely neutral on cancellation and return behavior — the 2-day delivery promise is neither retaining nor losing customers, suggesting the real problem lies in actual delivery execution (delays, carrier performance) rather than the promise itself.

8. customer retention vs first time buyer (we dont have full data for 2024 so comparing only based on 2025)

   2025 Average repeat rate → ~88-96%, Nearly 9 out of 10 orders in 2025 are from returning customers — QuickKart has a loyal and sticky customer base

   Repeat rate is consistently growing through 2025
        January 2025 → 78.48% repeat
        August  2025 → 94.26% repeat
        December 2025 → 96.76% repeat

   2025 December → only 3.24% first time customers (177 orders)

   QuickKart has excellent retention but weak acquisition — while 96% repeat rate sounds great, with only 177 new customers in December 2025







