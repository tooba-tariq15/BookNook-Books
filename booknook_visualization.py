import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns
import folium

load_dotenv()
password = os.environ["DB_PASSWORD"]
DATABASE_URL = f"postgresql+psycopg2://postgres:{password}@localhost:5432/booknook"
engine = create_engine(DATABASE_URL)

# --- Task 2.1: pull the joined DataFrame ---
query = """
SELECT o.order_id, o.order_date, o.status,
       p.product_name, p.category,
       oi.quantity, oi.unit_price
FROM orders o
JOIN orderitems oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
"""
df = pd.read_sql(query, engine)

df["order_date"] = pd.to_datetime(df["order_date"])
df["line_total"] = df["quantity"] * df["unit_price"]

print(df.head())
print(df.info())
print(df.describe())
print(df["category"].unique())

# --- Task 2.2: NumPy warm-up ---
values = df["line_total"].to_numpy()
avg_line_total = np.mean(values)
std_line_total = np.std(values)
above_avg_count = (values[values > avg_line_total]).size

print(f"Average order-line value: {avg_line_total:.2f}")
print(f"Standard deviation of order-line value: {std_line_total:.2f}")
print(f"Number of order-lines above average: {above_avg_count}")

# --- Task 2.3: trend and comparison charts ---
daily = df.groupby("order_date")["line_total"].sum()
daily_cumulative = daily.cumsum()
by_category = df.groupby("category")["line_total"].sum().sort_values(ascending=False)

# Chart 1 — Daily revenue (line)
plt.figure(figsize=(8, 5))
plt.plot(daily.index, daily.values, marker="o", color="blue")
plt.title("BookNook — Daily Revenue")
plt.xlabel("Date")
plt.ylabel("Revenue ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Chart 2 — Cumulative revenue (area)
plt.figure(figsize=(8, 5))
plt.fill_between(daily_cumulative.index, daily_cumulative.values, color="blue", alpha=0.4)
plt.plot(daily_cumulative.index, daily_cumulative.values, color="blue", linewidth=2)
plt.title("BookNook — Cumulative Revenue")
plt.xlabel("Date")
plt.ylabel("Total Revenue So Far ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Chart 3 — Revenue by category (bar)
plt.figure(figsize=(8, 5))
plt.bar(by_category.index, by_category.values, color="#ED7D31")
plt.title("BookNook — Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Revenue ($)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

# Chart 4 — Share of revenue by category (pie)
plt.figure(figsize=(6, 6))
plt.pie(
    by_category.values,
    labels=by_category.index,
    autopct="%1.1f%%",
    colors=["#1F4E79", "#2E75B6", "#9DC3E6", "#DEEBF7", "#BDD7EE", "#F4B183"],
)
plt.title("BookNook — Share of Revenue by Category")
plt.tight_layout()
plt.show()

# --- Task 2.4: distribution and relationship charts ---
by_product = df.groupby("product_name").agg(
    avg_price=("unit_price", "mean"),
    total_qty=("quantity", "sum"),
    revenue=("line_total", "sum")
).reset_index()

# Chart 5 — Histogram of line totals
plt.figure(figsize=(8, 5))
plt.hist(df["line_total"], bins=18, color="#4472C4", edgecolor="black")
plt.title("BookNook — Distribution of Order-Line Values")
plt.xlabel("Line Total ($)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# Chart 6 — Scatter: unit price vs quantity
plt.figure(figsize=(8, 5))
plt.scatter(df["unit_price"], df["quantity"], color="#ED7D31", alpha=0.7)
plt.title("BookNook — Unit Price vs Quantity")
plt.xlabel("Unit Price ($)")
plt.ylabel("Quantity")
plt.tight_layout()
plt.show()

# Chart 7 — Bubble chart: avg price vs total quantity, size = revenue
plt.figure(figsize=(8, 5))
plt.scatter(
    by_product["avg_price"],
    by_product["total_qty"],
    s=by_product["revenue"] * 3,
    color="#70AD47",
    alpha=0.6,
    edgecolor="black"
)
plt.title("BookNook — Books: Avg Price vs Total Quantity (bubble = revenue)")
plt.xlabel("Average Price ($)")
plt.ylabel("Total Quantity Sold")
plt.tight_layout()
plt.show()

# ============================================================
# DAY 3 — Seaborn, Folium, and the BookNook Story
# ============================================================

sns.set_theme(style="whitegrid")

# --- Task 3.1a: rebuild Day 2's bar chart in Seaborn ---
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="category", y="line_total", estimator="sum", errorbar=None)
plt.title("BookNook — Revenue by Category (Seaborn)")
plt.xlabel("Category")
plt.ylabel("Revenue ($)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

# --- Task 3.1b: new hue chart ---
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x="unit_price", y="quantity", hue="category", s=60, alpha=0.6)
plt.title("BookNook — Quantity vs Price, Colored by Category")
plt.xlabel("Unit Price ($)")
plt.ylabel("Quantity")
plt.tight_layout()
plt.show()

# --- Task 3.2: Folium map of customer cities ---
city_query = "SELECT city, COUNT(*) AS n FROM customers GROUP BY city;"
city_counts = pd.read_sql(city_query, engine)
print(city_counts)

city_coords = {
    "Islamabad":  (33.6844, 73.0479),
    "Lahore":     (31.5497, 74.3436),
    "Karachi":    (24.8607, 67.0011),
    "Rawalpindi": (33.5651, 73.0169),
    "Peshawar":   (34.0151, 71.5249),
    "Multan":     (30.1575, 71.5249),
}

m = folium.Map(location=[30.3753, 69.3451], zoom_start=5)

for _, row in city_counts.iterrows():
    city = row["city"]
    count = row["n"]
    if city in city_coords:
        lat, lon = city_coords[city]
        folium.CircleMarker(
            location=[lat, lon],
            radius=5 + count * 2,
            popup=f"{city}: {count} customers",
            color="#1F4E79",
            fill=True,
            fill_color="#2E75B6",
            fill_opacity=0.7,
        ).add_to(m)

m.save("booknook_customer_map.html")
print("Map saved to booknook_customer_map.html")