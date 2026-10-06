# Data and methods

The expected CSV columns are `order_id`, `customer_id`, `restaurant_name`, `cuisine_type`, `cost_of_the_order`, `day_of_the_week`, `rating`, `food_preparation_time`, and `delivery_time`. The day category is `Weekday` or `Weekend`; the rating is 1–5 or `Not given`. The loader rejects missing required values, duplicate order IDs, negative cost/time, and unexpected day or rating values.

- **Weekend cuisine volume:** Count orders within the weekend subset by cuisine. A Boolean comparison's length counts all weekend rows; it does not count matching cuisine rows.
- **Delivery time:** Mean of `delivery_time`, grouped by `day_of_the_week`. The data provide only a two-category day label, with no exact date, location, distance, driver capacity, or order timestamp.
- **End-to-end time:** `food_preparation_time + delivery_time`. Count strictly more than 60 minutes; exactly 60 is excluded.
- **Rating response:** `Not given` is an explicit category, not a null value. Missing ratings can bias averages for rated orders.
- **Illustrative commission:** 25% of order cost when cost is strictly greater than $20; 15% when cost is strictly greater than $5 and at most $20; zero otherwise. The brackets are mutually exclusive. This is an estimate from the exercise's assumed policy, not observed company revenue or net profit.
- **Promotion rule:** More than 50 *rated* orders and mean numeric rating strictly above 4; unrated orders do not count. This is an example eligibility rule, not a recommendation to deploy a campaign.

The provided dataset contains 1,898 orders, but its observation period and sampling method are unspecified. The analysis makes no causal inference or claim that these patterns generalize to other periods or markets. Restaurant and customer IDs stay out of the committed repository. The report includes only aggregate statistics from the private source data.
