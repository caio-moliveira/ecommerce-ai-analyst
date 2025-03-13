import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables for PostgreSQL credentials
load_dotenv()

# PostgreSQL configuration
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# Create a connection string
db_url = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
)

# Initialize database engine
engine = create_engine(db_url)
Base = declarative_base()
# Configurar a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)


# Define the SalesData table based on SalesRecord fields
class Sales(Base):
    __tablename__ = "my_sales"

    sale_date = Column(Date, nullable=False)
    sale_id = Column(String, primary_key=True, nullable=False)
    product_id = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    product_category = Column(String, nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    discount = Column(Integer, nullable=True)
    total_value = Column(Float, nullable=False)
    unit_cost = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)
    gross_profit = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False)
    payment_status = Column(String, nullable=False)
    payment_date = Column(Date, nullable=True)
    customer_id = Column(String, nullable=False)
    customer_name = Column(String, nullable=False)
    sales_channel = Column(String, nullable=False)
    sales_region = Column(String, nullable=False)
    sales_rep = Column(String, nullable=False)
    customer_rating = Column(String, nullable=True)
    shipping_cost = Column(Float, nullable=False)
    delivery_status = Column(String, nullable=False)
    delivery_date = Column(Date, nullable=True)


# Function to load all CSV files from the 'data' folder into PostgreSQL
def load_all_data_from_folder(folder_path="data", table_name="my_sales"):
    """Load all CSV files in the specified folder into the PostgreSQL database table."""
    try:
        if not os.path.exists(folder_path):
            print(f"Folder '{folder_path}' does not exist.")
            return

        files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

        if not files:
            print("No CSV files found in the folder.")
            return

        for file in files:
            file_path = os.path.join(folder_path, file)
            print(f"Processing file: {file_path}")
            load_data_to_postgres(file_path, table_name)
    except Exception as e:
        print(f"An error occurred while loading data from folder: {e}")


# Function to load a single CSV file into PostgreSQL
def load_data_to_postgres(file_path, table_name="my_sales"):
    """Load new data from a CSV file to a PostgreSQL database table, avoiding duplicates via unique constraint."""
    try:
        # Load CSV into a DataFrame
        df = pd.read_csv(file_path)

        # Insert new data into the PostgreSQL table, handling duplicates with the unique constraint
        with engine.connect() as connection:
            df.to_sql(table_name, connection, if_exists="append", index=False)
            print(
                f"New data from {file_path} loaded successfully into the '{table_name}' table."
            )
    except Exception as e:
        print(f"An error occurred while loading data to PostgreSQL: {e}")


if __name__ == "__main__":
    load_all_data_from_folder()
