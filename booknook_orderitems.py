import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text

load_dotenv()
password = os.environ["DB_PASSWORD"]
DATABASE_URL = f"postgresql+psycopg2://postgres:{password}@localhost:5432/booknook"


def sync_sequence(engine, table_name: str, id_column: str) -> None:
    with engine.begin() as conn:
        conn.execute(text(
            f"SELECT setval(pg_get_serial_sequence('{table_name}', '{id_column}'),"
            f"(SELECT MAX({id_column}) FROM {table_name}));"
        ))
    print(f"Synced auto-increment sequence for '{table_name}.{id_column}'")


def load_orderitems():
    engine = create_engine(DATABASE_URL)

    df = pd.read_csv("C:\\Users\\Tooba Tariq\\BookNook\\booknook_orderitems_seed.csv")
    df.to_sql("orderitems", con=engine, if_exists="append", index=False, method="multi")
    print(f"Loaded {len(df)} rows into orderitems")

    sync_sequence(engine, "orderitems", "order_item_id")


if __name__ == "__main__":
    load_orderitems()