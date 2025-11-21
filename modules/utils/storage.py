import logging

import pandas as pd
from load_django import *
from parser_app.models import Product


def save_to_database(product_data):
    """Save product data to the database."""
    try:
        product = Product.objects.create(**product_data)
        logging.info(f"Product saved to database with ID: {product.id}")
    except Exception as e:
        logging.error(f"Failed to save product to database: {e}")


def export_to_csv():
    """Export all products from the database to a CSV file."""
    try:
        products = Product.objects.all()
        df = pd.DataFrame(list(products.values()))
        df.to_csv("results/products.csv", index=False)
        logging.info("Products exported to CSV successfully.")
    except Exception as e:
        logging.error(f"Failed to export products to CSV: {e}")
