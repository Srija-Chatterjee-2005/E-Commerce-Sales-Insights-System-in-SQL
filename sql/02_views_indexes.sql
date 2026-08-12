DROP VIEW IF EXISTS v_order_lines_paid;
CREATE VIEW v_order_lines_paid AS
SELECT
  o.order_id,
  date(o.order_datetime) AS order_date,
  o.customer_id,
  o.channel_id,
  o.ship_country,
  o.ship_region,
  oi.product_id,
  oi.quantity,
  ROUND((oi.unit_price * oi.quantity) - oi.discount, 2) AS line_revenue,
  ROUND(p.cost_price * oi.quantity, 2) AS line_cost,
  ROUND(((oi.unit_price * oi.quantity) - oi.discount) - (p.cost_price * oi.quantity), 2) AS gross_profit
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
WHERE o.status = 'PAID';

DROP VIEW IF EXISTS v_order_summary;
CREATE VIEW v_order_summary AS
SELECT
  ol.order_id, ol.order_date, ol.customer_id, ol.channel_id, ol.ship_country, ol.ship_region,
  ROUND(SUM(ol.line_revenue),2) AS order_revenue,
  ROUND(SUM(ol.line_cost),2) AS order_cost,
  ROUND(SUM(ol.gross_profit),2) AS gross_profit,
  SUM(ol.quantity) AS units
FROM v_order_lines_paid ol
GROUP BY ol.order_id, ol.order_date, ol.customer_id, ol.channel_id, ol.ship_country, ol.ship_region;

DROP VIEW IF EXISTS v_channel_daily;
CREATE VIEW v_channel_daily AS
WITH rev AS (
  SELECT order_date, channel_id, SUM(order_revenue) AS revenue, COUNT(*) AS orders
  FROM v_order_summary GROUP BY order_date, channel_id
),
newcust AS (
  SELECT date(signup_at) AS dt, acquisition_channel_id AS channel_id, COUNT(*) AS new_customers
  FROM customers GROUP BY date(signup_at), acquisition_channel_id
)
SELECT
  ws.session_date AS order_date,
  c.channel_id,
  c.channel_name,
  ws.sessions,
  ws.conversions,
  ROUND(100.0 * ws.conversions / NULLIF(ws.sessions,0), 2) AS conversion_rate_pct,
  COALESCE(r.orders,0) AS orders,
  ROUND(COALESCE(r.revenue,0),2) AS revenue,
  ROUND(COALESCE(cs.spend,0),2) AS spend,
  ROUND(COALESCE(r.revenue,0) / NULLIF(cs.spend,0),2) AS roas,
  COALESCE(nc.new_customers,0) AS new_customers,
  ROUND(COALESCE(cs.spend,0) / NULLIF(nc.new_customers,0),2) AS cac
FROM website_sessions ws
JOIN channels c ON c.channel_id = ws.channel_id
LEFT JOIN rev r ON r.order_date = ws.session_date AND r.channel_id = ws.channel_id
LEFT JOIN channel_spend cs ON cs.spend_date = ws.session_date AND cs.channel_id = ws.channel_id
LEFT JOIN newcust nc ON nc.dt = ws.session_date AND nc.channel_id = ws.channel_id;

DROP VIEW IF EXISTS v_customer_lifetime_value;
CREATE VIEW v_customer_lifetime_value AS
SELECT c.customer_id, c.first_name || ' ' || c.last_name AS customer_name, c.country, c.region,
       COUNT(os.order_id) AS paid_orders,
       ROUND(COALESCE(SUM(os.order_revenue),0),2) AS lifetime_revenue,
       ROUND(COALESCE(AVG(os.order_revenue),0),2) AS avg_order_value,
       MIN(os.order_date) AS first_order_date,
       MAX(os.order_date) AS last_order_date
FROM customers c
LEFT JOIN v_order_summary os ON os.customer_id = c.customer_id
GROUP BY c.customer_id;

CREATE INDEX IF NOT EXISTS idx_orders_status_date ON orders(status, order_datetime);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_channel ON orders(channel_id);
CREATE INDEX IF NOT EXISTS idx_items_order ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_items_product ON order_items(product_id);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_spend_date_channel ON channel_spend(spend_date, channel_id);
CREATE INDEX IF NOT EXISTS idx_shipping_order ON shipping(order_id);
CREATE INDEX IF NOT EXISTS idx_returns_product ON returns(product_id);
