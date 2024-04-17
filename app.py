import streamlit as st
import logging

from billing.billing_main import main_billing
from products.product_main import main_product
from suppliers.supplier_main import main_supplier


def main():
    st.title("Billing Management System")
    st.sidebar.header("Menu")
    menu = st.sidebar.radio("Select Menu", ["Product", "Supplier", "Billing"])

    if menu == "Supplier":
        main_supplier()

    elif menu == "Product":
        main_product()

    elif menu == "Billing":
        main_billing()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
