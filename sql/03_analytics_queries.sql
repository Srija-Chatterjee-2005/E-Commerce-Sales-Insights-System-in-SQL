-- E-COMMERCE SALES INSIGHTS SYSTEM - ANALYTICS QUERY PACK
-- SQLite-compatible. Run in DB Browser for SQLite, sqlite3 CLI, or the included SQL Lab.

-- 1. Executive KPIs: orders, revenue, AOV, units, gross profit, margin
SELECT COUNT(*) AS paid_orders,
       ROUND(SUM(order_revenue),2) AS net_revenue,
       ROUND(AVG(order_revenue),2) AS aov,
       SUM(units) AS units_sold,
       ROUND(SUM(gross_profit),2) AS gross_profit,
       ROUND(100.0*SUM(gross_profit)/NULLIF(SUM(order_revenue),0),2) AS gross_margin_pct
FROM v_order_summary;

-- 2. Monthly sales trend
SELECT strftime('%Y-%m', order_date) AS month,
       COUNT(*) AS orders,
       ROUND(SUM(order_revenue),2) AS revenue,
       ROUND(AVG(order_revenue),2) AS aov
FROM v_order_summary
GROUP BY 1 ORDER BY 1;

-- 3. Channel performance: spend, revenue, ROAS, conversion and CAC
SELECT channel_name,
       SUM(sessions) AS sessions,
       SUM(conversions) AS conversions,
       ROUND(100.0*SUM(conversions)/NULLIF(SUM(sessions),0),2) AS conversion_rate_pct,
       ROUND(SUM(revenue),2) AS revenue,
       ROUND(SUM(spend),2) AS spend,
       ROUND(SUM(revenue)/NULLIF(SUM(spend),0),2) AS roas,
       SUM(new_customers) AS new_customers,
       ROUND(SUM(spend)/NULLIF(SUM(new_customers),0),2) AS cac
FROM v_channel_daily GROUP BY channel_name ORDER BY roas DESC;

-- 4. Top products by revenue and units
SELECT p.product_name, c.category_name,
       SUM(ol.quantity) AS units,
       ROUND(SUM(ol.line_revenue),2) AS revenue,
       ROUND(SUM(ol.gross_profit),2) AS gross_profit
FROM v_order_lines_paid ol
JOIN products p ON p.product_id=ol.product_id
JOIN categories c ON c.category_id=p.category_id
GROUP BY p.product_id ORDER BY revenue DESC LIMIT 10;

-- 5. Category profitability
SELECT c.category_name,
       ROUND(SUM(ol.line_revenue),2) AS revenue,
       ROUND(SUM(ol.gross_profit),2) AS gross_profit,
       ROUND(100.0*SUM(ol.gross_profit)/NULLIF(SUM(ol.line_revenue),0),2) AS margin_pct
FROM v_order_lines_paid ol
JOIN products p ON p.product_id=ol.product_id
JOIN categories c ON c.category_id=p.category_id
GROUP BY c.category_id ORDER BY gross_profit DESC;

-- 6. Geographic sales split
SELECT ship_country, ship_region, COUNT(*) AS orders,
       ROUND(SUM(order_revenue),2) AS revenue,
       ROUND(AVG(order_revenue),2) AS aov
FROM v_order_summary GROUP BY ship_country, ship_region ORDER BY revenue DESC;

-- 7. High-value customers
SELECT customer_id, customer_name, country, paid_orders, lifetime_revenue, avg_order_value
FROM v_customer_lifetime_value
WHERE paid_orders > 0 ORDER BY lifetime_revenue DESC LIMIT 20;

-- 8. Repeat customer rate
WITH x AS (SELECT customer_id, COUNT(*) AS n FROM v_order_summary GROUP BY customer_id)
SELECT COUNT(*) AS purchasing_customers,
       SUM(CASE WHEN n>=2 THEN 1 ELSE 0 END) AS repeat_customers,
       ROUND(100.0*SUM(CASE WHEN n>=2 THEN 1 ELSE 0 END)/COUNT(*),2) AS repeat_customer_rate_pct
FROM x;

-- 9. 30-day repeat purchase cohorts
WITH first_order AS (
  SELECT customer_id, MIN(order_date) AS first_dt FROM v_order_summary GROUP BY customer_id
), repeats AS (
  SELECT f.customer_id, f.first_dt,
         MAX(CASE WHEN julianday(o.order_date)>julianday(f.first_dt)
                   AND julianday(o.order_date)<=julianday(f.first_dt)+30 THEN 1 ELSE 0 END) AS repeated_30d
  FROM first_order f LEFT JOIN v_order_summary o ON o.customer_id=f.customer_id
  GROUP BY f.customer_id, f.first_dt
)
SELECT strftime('%Y-%m', first_dt) AS cohort_month,
       COUNT(*) AS cohort_customers,
       SUM(repeated_30d) AS repeat_30d_customers,
       ROUND(100.0*SUM(repeated_30d)/COUNT(*),2) AS repeat_30d_rate_pct
FROM repeats GROUP BY cohort_month ORDER BY cohort_month;

-- 10. Refund impact
SELECT strftime('%Y-%m', return_date) AS month, COUNT(*) AS returns,
       ROUND(SUM(refund_amount),2) AS refund_value
FROM returns GROUP BY month ORDER BY month;

-- 11. Shipping performance and late delivery rate
SELECT courier,
       COUNT(*) AS delivered_shipments,
       ROUND(AVG(julianday(delivered_at)-julianday(shipped_at)),2) AS avg_delivery_days,
       ROUND(100.0*SUM(CASE WHEN date(delivered_at)>promised_delivery_date THEN 1 ELSE 0 END)/COUNT(*),2) AS late_delivery_pct
FROM shipping WHERE shipping_status='DELIVERED' GROUP BY courier ORDER BY late_delivery_pct;

-- 12. Payment mix
SELECT method, COUNT(*) AS transactions,
       ROUND(SUM(paid_amount),2) AS amount,
       ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM payments),2) AS transaction_share_pct
FROM payments GROUP BY method ORDER BY amount DESC;

-- 13. Inventory risk - items at/below reorder level on latest snapshot
WITH latest AS (SELECT MAX(snapshot_date) AS dt FROM inventory_snapshots)
SELECT p.sku, p.product_name, i.stock_on_hand, i.reorder_level,
       CASE WHEN i.stock_on_hand<=i.reorder_level THEN 'REORDER' ELSE 'OK' END AS stock_flag
FROM inventory_snapshots i JOIN latest l ON i.snapshot_date=l.dt
JOIN products p ON p.product_id=i.product_id
ORDER BY stock_flag DESC, stock_on_hand ASC;

-- 14. Refund rate by category
SELECT c.category_name, COUNT(r.return_id) AS returned_lines,
       ROUND(SUM(r.refund_amount),2) AS refund_amount
FROM returns r JOIN products p ON p.product_id=r.product_id
JOIN categories c ON c.category_id=p.category_id
GROUP BY c.category_id ORDER BY refund_amount DESC;

-- 15. Revenue concentration: share of top 10 products
WITH p AS (
  SELECT product_id, SUM(line_revenue) AS rev FROM v_order_lines_paid GROUP BY product_id
), t AS (SELECT SUM(rev) AS total_rev FROM p), top AS (SELECT SUM(rev) AS top_rev FROM (SELECT rev FROM p ORDER BY rev DESC LIMIT 10))
SELECT ROUND(100.0*top.top_rev/t.total_rev,2) AS top10_revenue_share_pct FROM top,t;
