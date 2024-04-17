import streamlit as st
import psycopg2

from database_connection.database_connection import DatabaseConnection, db_connection


# Validating User Inputs:
def validate_inputs(purchase_id: int, supplier_id: int, gstin_number: str, product_id: int, quantity: int, unit_price: float,
                    total: float, discount: float, cgst: float, sgst: float, igst: float, purchase_date: str, item: str):
    if not purchase_id:
        st.warning("Please enter the Purchase ID")
        return False
    if not supplier_id:
        st.warning("Please enter existing Supplier ID")
        return False
    if not gstin_number.strip():
        st.warning("Please enter existing GSTIN Number")
        return False
    if not product_id:
        st.warning("Please enter existing Product ID")
        return False
    if quantity <= 0:
        st.warning("Please enter valid Quantity")
        return False
    if unit_price <= 0:
        st.warning("Please enter valid Unit Price")
        return False
    if total <= 0:
        st.warning("Please enter valid Total")
        return False
    if discount < 0:
        st.warning("Please enter valid Discount")
        return False
    if cgst < 0:
        st.warning("Please enter valid CGST")
        return False
    if sgst < 0:
        st.warning("Please enter valid SGST")
        return False
    if igst < 0:
        st.warning("Please enter valid IGST")
        return False
    if not purchase_date.strip():
        st.warning("Please enter the Purchase Date")
        return False
    if not item.strip():
        st.warning("Please enter the Item")
        return False


# Creating Billing Class:
class Billing:
    def __init__(self, connection):
        self.connection = connection

    def insert_purchase(self, purchase_id: int, supplier_id: int, gstin_number: str, product_id: int, quantity: int,
                        unit_price: float, total: float, discount: float, cgst: float, sgst: float, igst: float,
                        purchase_date: str, item: str):
        try:
            cursor = self.connection.cursor()
            postgres_insert_query = """INSERT INTO Purchase (purchase_id, supplier_id, gstin_number, product_id, quantity, unit_price, total, discount, cgst, sgst, igst, purchase_date, item) VALUES (%x,%x,%s,%x,%x,%f,%f,%f,%f,%f,%f,%s,%s)"""
            record_to_insert = (purchase_id, supplier_id, gstin_number, product_id, quantity, unit_price, total, discount,
                                cgst, sgst, igst, purchase_date, item)
            cursor.execute(postgres_insert_query, record_to_insert)
            self.connection.commit()
            count = cursor.rowcount
            st.success(f"{count} Record(s) inserted successfully into Purchase table")
        except (Exception, psycopg2.Error) as error:
            st.error("Failed to insert record into Purchase table: " + str(error))

    def update_purchase(self, purchase_id: int, supplier_id: int, gstin_number: str, product_id: int, quantity: int,
                        unit_price: float, total: float, discount: float, cgst: float, sgst: float, igst: float,
                        purchase_date: str, item: str):
        try:
            cursor = self.connection.cursor()
            postgres_update_query = """UPDATE Purchase SET supplier_id = %x, gstin_number = %s, product_id = %x, quantity = %x, unit_price = %f, total = %f, discount = %f, cgst = %f, sgst = %f, igst = %f, purchase_date = %s, item = %s WHERE purchase_id = %x"""
            record_to_update = (supplier_id, gstin_number, product_id, quantity, unit_price, total, discount, cgst, sgst,
                                igst, purchase_date, item, purchase_id)
            cursor.execute(postgres_update_query, record_to_update)
            self.connection.commit()
            count = cursor.rowcount
            st.success(f"{count} Record(s) updated successfully in Purchase table")
        except (Exception, psycopg2.Error) as error:
            st.error("Failed to update record in Purchase table: " + str(error))

    def delete_purchase(self, purchase_id: int):
        try:
            cursor = self.connection.cursor()
            postgres_delete_query = """DELETE FROM Purchase WHERE purchase_id = %x"""
            cursor.execute(postgres_delete_query, (purchase_id,))
            self.connection.commit()
            count = cursor.rowcount
            st.success(f"{count} Record(s) deleted successfully from Purchase table")
        except (Exception, psycopg2.Error) as error:
            st.error("Failed to delete record from Purchase table: " + str(error))


# Streamlit UI for Billing Management:
def main_billing():
    st.header("Purchase Billing Management")
    if db_connection is None:
        billing = Billing(db_connection)
        billing_menu = st.selectbox("Billing Menu", ["Insert", "Update", "Delete"], key="billing_menu", help="Select the operation you want to perform on the Purchase table")

        # Insert New Purchase Record:
        if billing_menu == "Insert":
            st.subheader("Insert New Purchase Record")
            purchase_id = st.number_input("Purchase ID", key="purchase_id", help="Enter the unique numeric ID for the new purchase record")
            supplier_id = st.number_input("Supplier ID", key="supplier_id", help="Enter the existing numeric ID of the supplier")
            gstin_number = st.text_input("GSTIN Number", key="gstin_number", help="Enter the existing GSTIN Number of the supplier")
            product_id = st.number_input("Product ID", key="product_id", help="Enter the existing numeric ID of the product")
            quantity = st.number_input("Quantity", key="quantity", help="Enter the quantity of the product purchased")
            unit_price = st.number_input("Unit Price", key="unit_price", help="Enter the unit price of the product")
            total = st.number_input("Total", key="total", help="Enter the total amount of the purchase")
            discount = st.number_input("Discount", key="discount", help="Enter the discount amount")
            cgst = st.number_input("CGST", key="cgst", help="Enter the CGST amount")
            sgst = st.number_input("SGST", key="sgst", help="Enter the SGST amount")
            igst = st.number_input("IGST", key="igst", help="Enter the IGST amount")
            purchase_date = st.date_input("Purchase Date", key="purchase_date", help="Select the date of the purchase")
            item = st.text_area("Item", key="item", help="Enter the item description")
            if st.button("Insert Purchase"):
                try:
                    if validate_inputs(purchase_id, supplier_id, gstin_number, product_id, quantity, unit_price, total,
                                       discount, cgst, sgst, igst, purchase_date, item):
                        billing.insert_purchase(purchase_id, supplier_id, gstin_number, product_id, quantity, unit_price,
                                                total, discount, cgst, sgst, igst, purchase_date, item)
                except Exception as e:
                    st.error("Failed to insert record into Purchase table: " + str(e))

        # Update Existing Purchase Record:
        elif billing_menu == "Update":
            st.subheader("Update Existing Purchase Record")
            purchase_id = st.number_input("Purchase ID", key="purchase_id", help="Enter the unique numeric ID of the purchase record you want to update")
            supplier_id = st.number_input("Supplier ID", key="supplier_id", help="Enter the updated numeric ID of the supplier")
            gstin_number = st.text_input("GSTIN Number", key="gstin_number", help="Enter the updated GSTIN Number of the supplier")
            product_id = st.number_input("Product ID", key="product_id", help="Enter the updated numeric ID of the product")
            quantity = st.number_input("Quantity", key="quantity", help="Enter the updated quantity of the product purchased")
            unit_price = st.number_input("Unit Price", key="unit_price", help="Enter the updated unit price of the product")
            total = st.number_input("Total", key="total", help="Enter the updated total amount of the purchase")
            discount = st.number_input("Discount", key="discount", help="Enter the updated discount amount")
            cgst = st.number_input("CGST", key="cgst", help="Enter the updated CGST amount")
            sgst = st.number_input("SGST", key="sgst", help="Enter the updated SGST amount")
            igst = st.number_input("IGST", key="igst", help="Enter the updated IGST amount")
            purchase_date = st.date_input("Purchase Date", key="purchase_date", help="Select the updated date of the purchase")
            item = st.text_area("Item", key="item", help="Enter the updated item description")
            if st.button("Update Purchase"):
                try:
                    if validate_inputs(purchase_id, supplier_id, gstin_number, product_id, quantity, unit_price, total,
                                       discount, cgst, sgst, igst, purchase_date, item):
                        billing.update_purchase(purchase_id, supplier_id, gstin_number, product_id, quantity, unit_price,
                                                total, discount, cgst, sgst, igst, purchase_date, item)
                except Exception as e:
                    st.error("Failed to update record in Purchase table: " + str(e))

        # Delete Existing Purchase Record:
        elif billing_menu == "Delete":
            st.subheader("Delete Existing Purchase Record")
            purchase_id = st.number_input("Purchase ID", key="purchase_id", help="Enter the unique numeric ID of the purchase record you want to delete")
            if st.button("Delete Purchase"):
                try:
                    billing.delete_purchase(purchase_id)
                except Exception as e:
                    st.error("Failed to delete record from Purchase table: " + str(e))

        # Close the database connection:
        billing.connection.close()
        st.info("Database connection closed successfully.")

    else:
        st.error("An error occurred while connecting to the database.")
