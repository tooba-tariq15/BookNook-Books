import pandas as pd 
from sqlalchemy import create_engine, text
DATABASE_URL = "postgresql+psycopg2://postgres:123456@localhost:5432/booknook"
DATA_DIR = r"C:\Users\Tooba Tariq\BookNook"

def load_seed_table(engine, csv_filename: str, table_name: str) -> None:
    csv_path = f"{DATA_DIR}\\{csv_filename}"
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, con=engine, if_exists = "append", index = False, method = "multi")
    print(f"Loaded {len(df)} rows from {csv_path} into {table_name}'")

def sync_sequence(engine, table_name:str, id_column: str) -> None:
    with engine.begin() as conn:
        conn.execute(text(
        f"SELECT setval (pg_get_serial_sequence ('{table_name}', '{id_column}'),"
        f"(SELECT MAX({id_column}) FROM {table_name}));"
        ))
    print (f"Synced auto-increment sequence for '{table_name}.{id_column}'")

def run_seed():
    engine = create_engine(DATABASE_URL)
    load_seed_table(engine, "booknook_customers_seed.csv", "customers")
    load_seed_table(engine, "booknook_products_seed.csv", "products")
    sync_sequence(engine, "customers", "customer_id")
    sync_sequence(engine, "products", "product_id")
    sync_sequence(engine, "customers", "customer_id")
    sync_sequence(engine, "products", "product_id")
    
    print("Seed data loaded successfully.")

if __name__ == "__main__":
    run_seed()
    