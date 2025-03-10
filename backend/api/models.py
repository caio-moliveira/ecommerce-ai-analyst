import uuid
from sqlalchemy import Column, Integer, String, Numeric, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

SALES_CHANNELS = ("Online", "In-Store", "Wholesale")
PAYMENT_STATUSES = ("Pending", "Completed", "Failed", "Refunded")
DELIVERY_STATUSES = ("Pending", "Shipped", "Delivered", "Cancelled")


class SalesData(Base):
    __tablename__ = "my_sales"

    sale_id = Column(
        String, primary_key=True, default=lambda: str(uuid.uuid4()), nullable=False
    )
    sale_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    product_id = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    product_category = Column(String, nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    discount = Column(Numeric(5, 2), nullable=True, default=0.00)
    total_value = Column(Numeric(10, 2), nullable=False)
    unit_cost = Column(Numeric(10, 2), nullable=False)
    total_cost = Column(Numeric(10, 2), nullable=False)
    gross_profit = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(String, nullable=False)
    payment_status = Column(
        Enum(*PAYMENT_STATUSES, name="payment_status_enum"), nullable=False
    )
    payment_date = Column(DateTime, nullable=True)
    customer_id = Column(String, nullable=False)
    customer_name = Column(String, nullable=False)
    customer_rating = Column(Integer, nullable=True)
    sales_channel = Column(
        Enum(*SALES_CHANNELS, name="sales_channel_enum"), nullable=False
    )
    sales_region = Column(String, nullable=False)
    sales_rep = Column(String, nullable=False)
    shipping_cost = Column(Numeric(10, 2), nullable=False)
    delivery_status = Column(
        Enum(*DELIVERY_STATUSES, name="delivery_status_enum"), nullable=False
    )
    delivery_date = Column(DateTime, nullable=True)
