import pandas as pd
import random
from faker import Faker
from datetime import timedelta, datetime
import os
import numpy as np

# Initialize Faker and set the number of rows
fake = Faker()

# Lists of random values for specific columns
product_categories = [
    "Fresh Produce",
    "Dairy Products",
    "Beverages",
    "Snacks",
    "Household Essentials",
]
products = [
    "Apples",
    "Bananas",
    "Carrots",
    "Spinach",
    "Milk",
    "Cheese",
    "Yogurt",
    "Butter",
    "Orange Juice",
    "Coffee",
    "Mineral Water",
    "Soda",
    "Potato Chips",
    "Chocolate Bar",
    "Nuts",
    "Crackers",
    "Dish Soap",
    "Paper Towels",
    "Laundry Detergent",
    "Trash Bags",
]
sales_channels = ["Online Store", "Marketplace", "Physical Store"]
payment_methods = ["Credit Card", "Pix", "Invoice", "Bank Transfer"]
payment_statuses = ["Paid", "Pending", "Canceled"]
delivery_statuses = ["Delivered", "In Transit", "Canceled"]
sales_regions = ["New York", "California", "Texas", "Florida", "Illinois"]
sales_reps = [fake.name() for _ in range(30)]

# Default start date and number of days to generate data
START_DATE = datetime(2024, 12, 31)
NUM_DAYS = 1  # Number of days to generate data for


def generate_random_record(sale_date):
    sale_id = fake.uuid4()
    product_id = f"PRD{random.randint(10000, 99999)}"
    product_name = random.choice(products)
    product_category = random.choice(product_categories)
    quantity_sold = random.randint(1, 10)
    unit_price = round(random.uniform(50, 500), 2)
    discount = random.choice([0, 5, 10, 15, 20])
    total_value = round(quantity_sold * unit_price * (1 - discount / 100), 2)
    unit_cost = round(unit_price * random.uniform(0.5, 0.8), 2)
    total_cost = round(quantity_sold * unit_cost, 2)
    gross_profit = round(total_value - total_cost, 2)
    payment_method = random.choice(payment_methods)
    payment_status = random.choice(payment_statuses)
    payment_date = (
        sale_date + timedelta(days=random.randint(0, 5))
        if payment_status == "Paid"
        else None
    )
    customer_id = f"CUS{random.randint(1000, 9999)}"
    customer_name = fake.name()
    sales_channel = random.choice(sales_channels)
    sales_region = random.choice(sales_regions)
    sales_rep = random.choice(sales_reps)
    customer_rating = random.choice(
        ["1 star", "2 stars", "3 stars", "4 stars", "5 stars"]
    )
    shipping_cost = round(random.uniform(5, 50), 2)
    delivery_status = random.choice(delivery_statuses)
    delivery_date = (
        sale_date + timedelta(days=random.randint(1, 10))
        if delivery_status == "Delivered"
        else None
    )

    return {
        "Sale Date": sale_date,
        "Sale ID": sale_id,
        "Product ID": product_id,
        "Product Name": product_name,
        "Product Category": product_category,
        "Quantity Sold": quantity_sold,
        "Unit Price": unit_price,
        "Discount (%)": discount,
        "Total Value (with Discount)": total_value,
        "Unit Cost": unit_cost,
        "Total Cost": total_cost,
        "Gross Profit": gross_profit,
        "Payment Method": payment_method,
        "Payment Status": payment_status,
        "Payment Date": payment_date,
        "Customer ID": customer_id,
        "Customer Name": customer_name,
        "Sales Channel": sales_channel,
        "Sales Region": sales_region,
        "Sales Representative": sales_rep,
        "Customer Rating": customer_rating,
        "Shipping Cost": shipping_cost,
        "Delivery Status": delivery_status,
        "Delivery Date": delivery_date,
    }


def generate_sales_data(num_days=NUM_DAYS):
    os.makedirs("data", exist_ok=True)  # Ensure data directory exists
    current_date = START_DATE

    for _ in range(num_days):
        num_rows = np.random.randint(10, 25)
        sales_data = [generate_random_record(current_date) for _ in range(num_rows)]
        df_sales = pd.DataFrame(sales_data)

        date_str = current_date.strftime("%Y%m%d")
        csv_path = f"data/sales_data_{date_str}.csv"

        df_sales.to_csv(csv_path, index=False, encoding="utf-8")
        print(f"File '{csv_path}' created successfully with {num_rows} rows.")

        current_date += timedelta(days=1)


if __name__ == "__main__":
    generate_sales_data()
