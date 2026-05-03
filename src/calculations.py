import pandas as pd

def get_customer_metrics(df):
    """
    Calculate monthly customer metrics from master df
    Returns monthly aggregated dataframe
    """
    # Step 1 - Order level (remove item level duplicates)
    orders_1 = (df[["order_id","customer_id","created_at",
                     "status","order_year","order_month","order_monthname"]]
                .drop_duplicates(subset="order_id")
                .copy())

    # Step 2 - Sort
    orders_1 = orders_1.sort_values(["customer_id","created_at"])

    # Step 3 - Customer order number
    orders_1["customer_order_num"] = (orders_1.groupby("customer_id")["order_id"]
                                       .cumcount() + 1)

    # Step 4 - Flags
    orders_1["delivered_flag"] = (orders_1["status"] == "Delivered").astype(int)
    orders_1["bad_flag"]       = orders_1["status"].isin(["Cancelled","Returned"]).astype(int)

    # Step 5 - Cumulative delivered per customer
    orders_1["cum_delivered"] = orders_1.groupby("customer_id")["delivered_flag"].cumsum()

    # Step 6 - Customer month level
    cust_month = (orders_1.groupby(["customer_id","order_year","order_month","order_monthname"])
                  .agg(first_order_num   =("customer_order_num","min"),
                       max_cum_delivered =("cum_delivered","max"))
                  .reset_index())

    # Step 7 - Mutually exclusive flags
    cust_month["is_first"]  = (cust_month["first_order_num"] == 1).astype(int)
    cust_month["is_repeat"] = (cust_month["max_cum_delivered"] >= 2).astype(int)
    cust_month["is_first"]  = cust_month["is_first"] * (1 - cust_month["is_repeat"])

    # Step 8 - Monthly aggregation
    final = (cust_month.groupby(["order_year","order_month","order_monthname"])
             .agg(total_customers      =("customer_id","nunique"),
                  first_time_customers =("is_first","sum"),
                  repeat_customers     =("is_repeat","sum"))
             .reset_index())

    # Step 9 - Total orders + bad orders
    orders_monthly = (orders_1.groupby(["order_year","order_month","order_monthname"])
                      .agg(total_orders =("order_id","nunique"),
                           bad_orders   =("bad_flag","sum"))
                      .reset_index())

    # Step 10 - Merge
    final = final.merge(orders_monthly,
                        on=["order_year","order_month","order_monthname"],
                        how="left")

    # Step 11 - Rates
    final["repeat_purchase_rate"] = (final["repeat_customers"] / 
                                      final["total_customers"] * 100).round(2)
    final["first_purchase_rate"]  = (final["first_time_customers"] / 
                                      final["total_customers"] * 100).round(2)
    final["bad_order_rate"]       = (final["bad_orders"] / 
                                      final["total_orders"] * 100).round(2)

    return final.sort_values(["order_year","order_month"]).reset_index(drop=True)