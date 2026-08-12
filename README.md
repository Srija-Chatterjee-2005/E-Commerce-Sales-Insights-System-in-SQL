# **🛒 E-Commerce Sales Insights System**
---

SQL-Driven E-Commerce Analytics • Interactive Dashboard • Real-TimeCustom Query Execution

The E-Commerce Sales Insights System is a portfolio-focused dataanalytics project that transforms structured e-commerce transaction datainto meaningful business insights. It combines a normalized relationaldatabase, analytical SQL, reusable views, performance-oriented indexes,and an interactive local dashboard for sales, customer, product,marketing, profitability, retention, refund, shipping, payment, andinventory analysis.

The portfolio version uses SQLite, so it runs locally withoutrequiring Oracle, MySQL, PostgreSQL, Docker, or a separate databaseserver.

<img width="1900" height="1021" alt="Screenshot 2026-08-12 011309" src="https://github.com/user-attachments/assets/f089d8ef-9969-4ef5-abe3-417219153659" />


## **🎯A. Project Objective**
---

The objective is to design a relational e-commerce database and use SQLanalytics to monitor:

Revenue and sales performance

Average Order Value (AOV)

Conversion rate

Marketing ROAS and CAC

Customer cohorts and repeat purchases

Top products and categories

Regional performance

Gross profit and profitability

Refund and return impact

Shipping performance

Inventory risk

The system demonstrates how raw e-commerce data can be converted intostructured, decision-ready business intelligence.


<img width="1913" height="946" alt="Screenshot 2026-08-12 011332" src="https://github.com/user-attachments/assets/8db2c747-c216-4522-8dec-166b2b572aaa" />


---


## **💼B. Industry Relevance**
---

E-commerce businesses depend on analytics to understand what isselling, who is buying, which channels are performing, where profit isgenerated, and where operational issues exist.

Metrics such as ROAS, CAC, AOV, conversion rate, repeat-customer rate,gross margin, refund impact, and delivery performance supportdecisions related to pricing, inventory, customer retention, advertisingbudgets, and operations.

## **🧰C. Tools & Technologies**
---
          

SQLite    

Relational database and SQL executionSQL        

Data modeling, 

KPI calculations and analytics

Python         

Local dashboard and application logic

HTML/CSS/JavaScript   

Dashboard interface and interactivity CSV    

Portable source-data exports

Git & GitHub        

Version control and publishing


<img width="1919" height="931" alt="Screenshot 2026-08-12 011340" src="https://github.com/user-attachments/assets/649eb894-ec39-4a6d-8207-98463720c63a" />


---

## **🔄D. Project Workflow**
---

Synthetic E-Commerce Data⬇️Relational Database Design⬇️Data Validation & Constraints⬇️SQL Views & Indexes⬇️Business KPI Queries⬇️Sales / Marketing / Customer / Product / Operations Analysis⬇️Interactive Dashboard⬇️Pre-Built Query Library + Custom SQL Execution⬇️Business Insights & Decision Support

---

## **📁E. Project Structure**
---

<img width="595" height="781" alt="Screenshot 2026-08-12 114800" src="https://github.com/user-attachments/assets/e6ed589e-0994-439a-9605-9931e2c29324" />


---

## **🗄️F. Database Design**
---

The normalized relational structure includes:

Customers -- profile, geography, signup and acquisitioninformation

Categories -- product-category master

Products -- SKU, product, cost and list price

Channels -- marketing/acquisition channels

Channel Spend -- daily advertising activity and spend

Website Sessions -- sessions, carts, checkouts and conversions

Orders -- customer orders, status, channel and destination

Order Items -- quantity, selling price and discounts

Payments -- payment amount, method and transaction status

Shipping -- courier, promised/delivery dates, cost and status

Returns -- return reasons and refund values

Inventory -- stock levels and inventory-risk information

Primary keys, foreign keys, constraints, reusable views, and indexessupport data integrity and analytical performance.

---

## **📊G. Dataset**
---

The project uses a synthetic e-commerce dataset created forportfolio demonstration and SQL analysis.

Metric                                Value

Customers                               700Products                                 31Product Categories                        6Total Orders                            949Paid Orders                             838Units Sold                            1,786Data Period            January -- June 2026

Note: All customer, order, marketing, shipping, and return data issynthetic and does not represent real individuals or companies.


<img width="1917" height="941" alt="Screenshot 2026-08-12 011405" src="https://github.com/user-attachments/assets/805ce9f0-f929-4e19-a329-f6f42e670a35" />


---

## **✨H. Key Features**
---

### **📈 Sales & Revenue Analytics**

Total and net revenue

Average Order Value

Monthly sales trends

Gross profit and margin

Product/category performance

Regional sales analysis

### **📣 Marketing Analytics**

Revenue by channel

Marketing spend

ROAS

CAC

Website sessions

Conversion rate

### **👥 Customer Analytics**

Customer Lifetime Value

High-value customers

Repeat-customer analysis

First-purchase cohorts

30-day repeat-purchase analysis

### **📦 Product & Inventory Analytics**

Top-selling products

Category profitability

Units sold

Revenue contribution

Inventory/reorder risk

### **🚚 Operations Analytics**

Courier performance

Average delivery time

Late-delivery rate

Refund and return analysis

Payment-method performance

## **🧠I. SQL Concepts Used**
---

SELECT, WHERE, ORDER BY

INNER JOIN, LEFT JOIN

GROUP BY and aggregate functions

SUM(), COUNT(), AVG(), MIN(), MAX()

Common Table Expressions (CTEs)

Subqueries

Conditional aggregation

Date-based analysis

NULLIF() for safe KPI calculations

Primary and foreign keys

CHECK constraints

Reusable SQL views

Indexes for query optimization


<img width="1919" height="961" alt="Screenshot 2026-08-12 011416" src="https://github.com/user-attachments/assets/611658cd-108d-4547-aabe-62a0370f6033" />


---


## **⚡J. Core Business KPIs**
---

Net Revenue

Total Orders

Average Order Value (AOV)

Units Sold

Gross Profit

Gross Margin

ROAS

CAC

Conversion Rate

Repeat-Customer Rate

30-Day Cohort Retention

Refunded Revenue

Late-Delivery Rate

---

## **📸K. Screenshots**
---

<img width="1919" height="906" alt="Screenshot 2026-08-12 011537" src="https://github.com/user-attachments/assets/87f275df-6337-48ab-a4d4-be53ef0f5f07" />
<img width="1910" height="918" alt="Screenshot 2026-08-12 011508" src="https://github.com/user-attachments/assets/4adbced8-c1ef-40ff-9df4-2bb89d51ef05" />
<img width="1917" height="904" alt="Screenshot 2026-08-12 011457" src="https://github.com/user-attachments/assets/84c58b90-56f2-4e76-bd7e-b055e06b8fa2" />
<img width="1918" height="869" alt="Screenshot 2026-08-12 011453" src="https://github.com/user-attachments/assets/c4581eb3-265c-4fff-974f-b3f562496ebd" />
<img width="1898" height="945" alt="Screenshot 2026-08-12 011427" src="https://github.com/user-attachments/assets/838f0d4c-84f6-4535-8a9c-364a200979af" />


---


## **🖥️L. Interactive Dashboard**
---

### **📊 Overview**

Revenue, orders, AOV, gross profit, margin, trends, products, andgeographic insights.

### **📣 Marketing**

Channel revenue, spend, ROAS, CAC, website sessions, and conversion.

### **🛍️ Products**

Product/category revenue, units, profitability, and inventory risk.

### **👥 Customers**

Customer LTV, repeat purchases, and cohort analysis.

### **🚚 Operations**

Shipping, late deliveries, returns, refunds, and payment methods.

### **💻 Interactive SQL Lab**

A combined pre-built Query Library + custom user SQL workspace.


---


## **💻M. Interactive SQL Lab -- Two Query Modes**
---

The SQL Lab is one of the main interactive features.

### **1️⃣ Pre-Built Query Library**

The application provides professionally prepared default SQL analyses. Auser can select one and run it immediately.

Examples include:

Revenue & AOV

Marketing ROAS

Top Products

Top Customers

Category Performance

Shipping Performance

Refund Analysis

Customer/Cohort Analysis

This creates a ready-made analytical layer for important businessquestions.

### **2️⃣ Custom User Query Execution**

A user can also write or modify an independent SQL query in theworkspace.

After clicking Run Query, the application:

Sends the query to the bundled SQLite database.

Executes it against the current project data.

Displays the resulting rows immediately.

Shows the returned row count.

Displays query execution time.

### **Example:**

SELECT product_name, list_price
FROM products
WHERE list_price > 50
ORDER BY list_price DESC;

The SQL Lab is intentionally read-only. Analytical SELECT / WITHstatements are supported while database-changing commands such asDELETE, UPDATE, DROP, and ALTER are blocked.

Real-time result means the query is executed when the user runs itand the result is calculated immediately from the local SQLitedatabase. It does not claim that live transactions are streamed froman external e-commerce platform.


<img width="1919" height="948" alt="Screenshot 2026-08-12 011630" src="https://github.com/user-attachments/assets/d3ad84bf-7973-4d51-a39e-7a6cd9b4d9d4" />


---

## **🎥N. How to Run**
---






https://github.com/user-attachments/assets/0b59bdf9-0c16-46c2-a088-b0c723c89865






---

## **🔎O. Core SQL Analytics**
---

The project includes SQL analyses for:

Revenue, orders, AOV and margin

Monthly revenue trends

Marketing ROAS, CAC and conversion

Top products

Category profitability

Geographic performance

High-value customers

Repeat customers

First-purchase cohorts and 30-day repeats

Refund impact

Courier/delivery performance

Payment-method analysis

Inventory risk

Category return analysis

Revenue concentration

---

## **📌P. Key Insights**
---

The system can identify:

Highest-revenue products and categories

Category profitability

Revenue versus advertising spend by channel

High-revenue versus high-efficiency channels

Valuable repeat customers

Retention through cohort analysis

Geographic order/revenue patterns

Refund and return patterns

Courier-level delivery performance

Products requiring inventory attention

The focus is not only SQL output, but converting analytical results intobusiness-relevant insights.


<img width="1891" height="1029" alt="Screenshot 2026-08-12 011658" src="https://github.com/user-attachments/assets/e938bd12-8e46-4b00-887b-b4b976b044a7" />

---

## **🚀Q. GitHub Upload Steps**
---

dir

cd ECommerce_Sales_Insights_System

git init

git add .

git commit -m "Initial commit - E-Commerce Sales Insights System"

git branch -M main

git remote add origin https://github.com/Srija-Chatterjee-2005/ecommerce-sales-insights-system.git

git push -u origin main

---

## **🔮R. Future Enhancements**
---

PostgreSQL/cloud warehouse migration

Automated ETL and scheduled refresh

Advanced customer segmentation

Sales forecasting

Product recommendation logic

Multi-touch marketing attribution

Role-based dashboard access

Automated data-quality checks

Cloud deployment

Power BI/Tableau integration

---

## **📄S. Project Report**
---

A detailed Project Report PDF has been included in the docs/ folderto document the architecture, KPI definitions, analytical logic,interactive SQL functionality, optimization techniques, businessinsights, and future enhancements.

---

## **✅T. Conclusion**
---

The E-Commerce Sales Insights System demonstrates an end-to-end SQLanalytics workflow---from relational database design and KPI developmentto interactive visualization and ad hoc query execution.

The combination of a pre-built analytical Query Library and acustom read-only SQL workspace with immediate results supports bothready-made business reporting and flexible user-driven analysis.

---

## **👩‍💻U. Author**
---

### **Srija Chatterjee**

GitHub: https://github.com/Srija-Chatterjee-2005

LinkedIn: https://www.linkedin.com/in/srija-chatterjee-82a539308?utm_source=share_via&utm_content=profile&utm_medium=member_android

---
