# Interview-Ready Q&A

**Q1: Explain your project.**  
**A1:** My project is an E-Commerce Sales Insights System built as a SQL-first analytics solution. I designed a normalized relational database covering customers, products, categories, orders, order items, payments, marketing channels, website sessions, shipping, returns and inventory. On top of the database, I created reusable SQL views and analytical queries for revenue, AOV, gross margin, ROAS, CAC, conversion, top products, geographic performance, high-value customers, cohorts, refunds and delivery performance. I then connected those insights to a lightweight local dashboard. I used SQLite for the portfolio package so the project runs without a database server, while keeping the model transferable to PostgreSQL or a BI tool.

**Q2: Why did you use a normalized relational design?**  
**A2:** I separated entities such as customers, products, orders and order items so each fact is stored in one logical place. Primary and foreign keys preserve relationships, reduce duplication and make joins reliable. For example, product cost is stored in Products while the selling price at the time of purchase is stored in Order_Items, which preserves historical transaction accuracy.

**Q3: Which SQL concepts did you use?**  
**A3:** I used joins, aggregations, GROUP BY, CTEs, conditional aggregation, subqueries, views, indexes and date functions. The dashboard KPIs are not hard-coded; they are calculated from relational data using SQL.

**Q4: How do you calculate revenue, AOV and gross margin?**  
**A4:** Line revenue is unit price multiplied by quantity minus discount. Net paid revenue is the sum of line revenue for PAID orders. AOV is paid revenue divided by paid order count. Gross profit is revenue minus product cost, and gross margin percentage is gross profit divided by revenue.

**Q5: How do you evaluate marketing channels?**  
**A5:** I combine website sessions, conversions, channel spend, customer acquisition and attributed order revenue. ROAS is revenue divided by spend, CAC is spend divided by new customers, and conversion rate is conversions divided by sessions. Looking at all three prevents judging a channel only by revenue.

**Q6: How did you perform cohort or retention analysis?**  
**A6:** I first calculate each customer's first paid order date. Then I check whether the same customer places another paid order within 30 days. Grouping first-order dates into monthly cohorts gives cohort size, repeat customers and 30-day repeat rate.

**Q7: How did you think about query optimization?**  
**A7:** I created indexes on columns used frequently in joins and filters, including order date/status, customer ID, channel ID, order-item foreign keys, product category, spend date/channel and shipping/return keys. I also created reusable views to simplify repeated analytical logic and kept dashboard queries selective.

**Q8: What operational insights are included beyond sales?**  
**A8:** The system measures late-delivery rate and average delivery time by courier, return reasons and refund value, payment method mix, and inventory items that have reached reorder level. This extends the project from a sales report into a broader e-commerce decision-support system.

**Q9: Why SQLite instead of PostgreSQL?**  
**A9:** PostgreSQL would be a strong production choice, but for a portable portfolio project I used SQLite because it is serverless and the database can be shipped as one file. The project still demonstrates relational modeling, SQL analytics, constraints, views and indexes. I can migrate the design to PostgreSQL by changing a small set of dialect-specific date and identity-column syntax.

**Q10: What would you improve next?**  
**A10:** I would connect a production PostgreSQL database to Power BI, introduce automated ETL from transactional sources, add customer segmentation and forecasting, create role-based access, and validate attribution across first-touch and multi-touch models. I would also add monitoring for data quality and scheduled refreshes.
