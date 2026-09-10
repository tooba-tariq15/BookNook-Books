import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd
from datetime import datetime

load_dotenv()
password = os.environ["DB_PASSWORD"]
DATABASE_URL = f"postgresql+psycopg2://postgres:{password}@localhost:5432/booknook"
engine = create_engine(DATABASE_URL)


def parse_date(value):
    for fmt in ("%Y-%m-%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(str(value).strip(), fmt).date()
        except ValueError:
            continue
    return pd.NaT


def extract():
    raw = pd.read_csv("C:\\Users\\Tooba Tariq\\BookNook\\booknook_raw_orders.csv")
    print(f"Read {len(raw)} rows")
    return raw


def transform(raw, engine):
    raw["customer_email"] = raw["customer_email"].str.strip().str.lower()
    raw["order_date"] = raw["order_date"].apply(parse_date)

    with engine.connect() as conn:
        rows = conn.execute(text("SELECT customer_id, email FROM customers;"))
        customer_lookup = {r.email: r.customer_id for r in rows}

    before = len(raw)
    raw = raw.dropna(subset=["order_date"])
    raw = raw[raw["customer_email"].isin(customer_lookup.keys())]
    print(f"Dropped {before - len(raw)} unsafe row(s).")

    raw["customer_id"] = raw["customer_email"].map(customer_lookup)
    return raw


def load(raw, engine):
    with engine.begin() as conn:
        for _, row in raw.iterrows():
            conn.execute(
                text("""
                    INSERT INTO orders (customer_id, order_date, status)
                    VALUES (:customer_id, :order_date, :status)
                    RETURNING order_id;
                """),
                {
                    "customer_id": int(row.customer_id),
                    "order_date": row.order_date,
                    "status": row.status,
                }
            )
    print(f"Loaded {len(raw)} orders")


def run_pipeline():
    raw = extract()
    raw = transform(raw, engine)
    load(raw, engine)


if __name__ == "__main__":
    run_pipeline()