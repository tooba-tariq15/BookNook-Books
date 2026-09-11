# 📚 BookNook Books — ETL Pipeline & Data Visualization Capstone

## 📌 Overview
An end-to-end data engineering and analytics project featuring an automated Python ETL pipeline and customized visualization scripts to process raw bookstore order data, manage database tables, and generate analytical charts.

## 🎯 Objective
To ingest, clean, transform, and load bookstore transactional data into a structured database workflow, and generate insightful visualizations examining pricing, revenue, and customer order patterns.

## 📄 Repository Structure & Files
* **Python Scripts & Pipeline**
  * `booknook_etlpipeline.py` — orchestrates the end-to-end ETL workflow
  * `booknook_dataimport.py` — handles data importing tasks
  * `booknook_createtables.py` — handles table creation routines
  * `booknook_orderitems.py` — processes order item logic
  * `booknook_visualization.py` — generates analytical charts and plots
* **Database & Queries**
  * `booknook_schema.sql` — database schema definition
  * `booknook_queries.sql` — analytical SQL queries
* **Datasets & Seeds**
  * `booknook_raw_orders.csv` — raw incoming order data
  * `booknook_customers_seed.csv` — customer seed dataset
  * `booknook_orderitems_seed.csv` — order items seed dataset
  * `booknook_products_seed.csv` — product catalog seed dataset
* **Visualizations & Outputs**
  * `Avg Price vs Total Quantity.PNG`
  * `Comulative Revenue.PNG`
  * `Distribution of Order-Line Values.PNG`
  * `Line Chart.PNG`
  * `Quantity vs Price - Seaborn.PNG`
  * `Revenue by Category - Seaborn.PNG`
  * `Revenue by Category.PNG`
  * `Share of Revenue by Category.PNG`
  * `Unit Price vs Quantity.PNG`
  * `booknook_customer_map.html` — interactive geographical customer map

## 🛠️ Tools & Skills Used
* Python (Pandas, Seaborn, Matplotlib)
* SQL & Relational Database Design
* ETL Pipeline Development & Data Automation
* Exploratory Data Analysis & Visualization

## 🚀 How to Run
1. Clone the repository to your local environment.
2. Execute the setup scripts (`booknook_createtables.py` or `booknook_schema.sql`) to prepare your database environment.
3. Run `booknook_etlpipeline.py` to process the raw CSV data and load it into the database.
4. Run `booknook_visualization.py` to generate the analytical charts and outputs.

## 📬 Connect With Me
* LinkedIn: [www.linkedin.com/in/tooba-tariq-]
* Email: [toobatariq114@gmail.com]

⭐ If you found this project helpful, feel free to star this repository!
