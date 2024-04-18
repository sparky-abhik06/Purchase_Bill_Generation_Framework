import pandas as pd
import streamlit as st
import psycopg2

from database_connection.database_connection import DatabaseConnection


# Validating User Inputs:
def validate_inputs(purchase_id: int, supplier_id: int, gstin_number: str, product_id: int, quantity: int, unit_price: float, total_price: float,
                    discount: float, cgst: float, sgst: float, igst: float, amount: float, purchase_date: str, item_description: str):
    if not purchase_id or purchase_id <= 0:
        st.warning("Please enter the Purchase ID")
        return False
    if not supplier_id or supplier_id <= 0:
        st.warning("Please enter existing Supplier ID")
        return False
    if not gstin_number.strip():
        st.warning("Please enter existing GSTIN Number")
        return False
    if not product_id or product_id <= 0:
        st.warning("Please enter existing Product ID")
        return False
    if quantity <= 0:
        st.warning("Please enter valid Quantity")
        return False
    if unit_price <= 0.0:
        st.warning("Please enter valid Unit Price")
        return False
    if total_price <= 0.0:
        st.warning("Please enter valid Total Price")
        return False
    if discount < 0.0:
        st.warning("Please enter valid Discount")
        return False
    if cgst < 0.0:
        st.warning("Please enter valid CGST")
        return False
    if sgst < 0.0:
        st.warning("Please enter valid SGST")
        return False
    if igst < 0.0:
        st.warning("Please enter valid IGST")
        return False
    if amount <= 0.0:
        st.warning("Please enter valid Amount")
        return False
    if not purchase_date.strip():
        st.warning("Please enter the Purchase Date")
        return False
    if not item_description.strip():
        st.warning("Please enter the Item")
        return False


# Creating Billing Class:
class Billing:
    def __init__(self, connection):
        self.connection = connection

    def insert_purchase(self, purchase_id: int, supplier_id: int, gstin_number: str, product_id: int, quantity: int,
                        unit_price: float, total_price: float, discount: float, cgst: float, sgst: float, igst: float,
                        amount: float, purchase_date: str, item_description: str):
        try:
            cursor = self.connection.cursor()
            postgres_insert_query = """INSERT INTO Purchase (purchase_id, supplier_id, gstin_number, product_id, quantity, unit_price, total, discount, cgst, sgst, igst, amount, purchase_date, item_description) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            record_to_insert = (purchase_id, supplier_id, gstin_number, product_id, quantity, unit_price, total_price, discount,
                                cgst, sgst, igst, amount, purchase_date, item_description)
            cursor.execute(postgres_insert_query, record_to_insert)
            self.connection.commit()
            count = cursor.rowcount
            st.success(f"{count} Record(s) inserted successfully into Purchase table")
        except (Exception, psycopg2.Error) as error:
            st.error("Failed to insert record into Purchase table: " + str(error))

    def update_purchase(self, purchase_id: int, supplier_id: int, gstin_number: str, product_id: int, quantity: int,
                        unit_price: float, total_price: float, discount: float, cgst: float, sgst: float, igst: float,
                        amount: float, purchase_date: str, item_description: str):
        try:
            cursor = self.connection.cursor()
            postgres_update_query = """UPDATE Purchase SET supplier_id = %s, gstin_number = %s, product_id = %s, quantity = %s, unit_price = %s, total_price = %s, discount = %s, cgst = %s, sgst = %s, igst = %s, amount = %s, purchase_date = %s, item_description = %s WHERE purchase_id = %s"""
            record_to_update = (supplier_id, gstin_number, product_id, quantity, unit_price, total_price, discount, cgst, sgst,
                                igst, amount, purchase_date, item_description, purchase_id)
            cursor.execute(postgres_update_query, record_to_update)
            self.connection.commit()
            count = cursor.rowcount
            st.success(f"{count} Record(s) updated successfully in Purchase table")
        except (Exception, psycopg2.Error) as error:
            st.error("Failed to update record in Purchase table: " + str(error))

    def delete_purchase(self, purchase_id: int):
        try:
            cursor = self.connection.cursor()
            postgres_delete_query = """DELETE FROM Purchase WHERE purchase_id = %s"""
            cursor.execute(postgres_delete_query, (purchase_id,))
            self.connection.commit()
            count = cursor.rowcount
            st.success(f"{count} Record(s) deleted successfully from Purchase table")
        except (Exception, psycopg2.Error) as error:
            st.error("Failed to delete record from Purchase table: " + str(error))

    def show_all_purchase(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""SELECT * FROM Purchase""")
            purchase_records = cursor.fetchall()
            if len(purchase_records) > 0:
                return purchase_records
            else:
                st.info("No records found in Purchase table")
                return None
        except (Exception, psycopg2.Error) as error:
            st.error("Failed to fetch records from Purchase table: " + str(error))
            return None

    def get_gstin_number(self, supplier_id: int):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""SELECT gstin_number FROM Supplier WHERE supplier_id = %s""", (supplier_id,))
            gstin_number = cursor.fetchone()
            if gstin_number:
                return gstin_number[0]
            else:
                st.info("No records found in Supplier table")
                return None
        except (Exception, psycopg2.Error) as error:
            st.error("Failed to fetch records from Supplier table: " + str(error))
            return None

    def get_product_price(self, product_id: int):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""SELECT unit_price FROM Product WHERE product_id = %s""", (product_id,))
            unit_price = cursor.fetchone()
            if unit_price:
                return unit_price[0]
            else:
                st.info("No records found in Product table")
                return None
        except (Exception, psycopg2.Error) as error:
            st.error("Failed to fetch records from Product table: " + str(error))
            return None

    def get_item(self, product_id: int):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""SELECT product_name, description, category FROM Product WHERE product_id = %s""", (product_id,))
            item = cursor.fetchone()
            if item:
                item_description = f"Product Name: {item[0]}\nDescription: {item[1]}\nCategory: {item[2]}"
                return item_description
            else:
                st.info("No records found in Product table")
                return None
        except (Exception, psycopg2.Error) as error:
            st.error("Failed to fetch records from Product table: " + str(error))
            return None

    def purchase_details(self, purchase_id: int):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""SELECT * FROM Purchase WHERE purchase_id = %s""", (purchase_id,))
            purchase_record = cursor.fetchone()
            if purchase_record:
                return purchase_record
            else:
                st.info("No records found in Purchase table")
                return None
        except (Exception, psycopg2.Error) as error:
            st.error("Failed to fetch records from Purchase table: " + str(error))
            return None


# Streamlit UI for Billing Management:
def main_billing():
    # Initialize session state
    if 'db_connection' not in st.session_state:
        st.session_state.db_connection = DatabaseConnection().connect()
    st.header("Purchase Billing Management")
    try:
        billing = Billing(st.session_state.db_connection)
        if billing.connection is not None:
            billing_menu = st.selectbox("Billing Menu", ["Insert", "Show All", "Update", "Delete"], key="billing_menu", help="Select the operation you want to perform on the Purchase table")

            # Insert New Purchase Record:
            if billing_menu == "Insert":
                st.subheader("Insert New Purchase Record")
                purchase_id = st.number_input("Purchase ID", value=None, placeholder="Type a number...", step=1, key="purchase_id", help="Enter the unique numeric ID for the new purchase record")
                supplier_id = st.number_input("Supplier ID", value=None, placeholder="Type a number...", step=1, key="supplier_id", help="Enter the existing numeric ID of the supplier")
                get_gstin_number = billing.get_gstin_number(supplier_id) if supplier_id else None
                gstin_number = st.text_input("GSTIN Number", value=get_gstin_number, key="gstin_number", help="Enter the existing GSTIN Number of the supplier", disabled=True)
                product_id = st.number_input("Product ID", value=None, placeholder="Type a number...", step=1, key="product_id", help="Enter the existing numeric ID of the product")
                quantity = st.number_input("Quantity", value=1, step=1, key="quantity", help="Enter the quantity of the product purchased")
                product_price = billing.get_product_price(product_id) if product_id else None
                unit_price = st.number_input("Unit Price", value=product_price, key="unit_price", help="Enter the unit price of the product", disabled=True)
                tot_price = (quantity * unit_price) if quantity and unit_price else 0.0
                total_price = st.number_input("Total Price", value=tot_price, key="total_price", help="Calculate the total price of the purchase", disabled=True)
                discount = st.number_input("Discount", value=0.0, key="discount", help="Enter the discount amount")
                cgst = st.number_input("CGST", value=0.0, key="cgst", help="Enter the CGST amount")
                sgst = st.number_input("SGST", value=0.0, key="sgst", help="Enter the SGST amount")
                igst = st.number_input("IGST", value=0.0, key="igst", help="Enter the IGST amount")
                final_amount = (total_price - discount + cgst + sgst + igst)
                amount = st.number_input("Amount", value=final_amount, key="amount", help="Calculate the total amount of the purchase", disabled=True)
                purchase_date = st.date_input("Purchase Date", key="purchase_date", help="Select the date of the purchase")
                item = billing.get_item(product_id) if product_id else None
                item_description = st.text_area("Item", value=item, key="item", help="Enter the item description")
                if st.button("Insert Purchase"):
                    try:
                        if validate_inputs(purchase_id, supplier_id, gstin_number, product_id, quantity, unit_price, total_price,
                                           discount, cgst, sgst, igst, amount, purchase_date, item_description):
                            billing.insert_purchase(purchase_id, supplier_id, gstin_number,
                                                    product_id, quantity, unit_price,
                                                    total_price, discount, cgst, sgst,
                                                    igst, amount, purchase_date, item_description)
                    except Exception as e:
                        st.error("Failed to insert record into Purchase table: " + str(e))

            # Show All Purchase Records:
            elif billing_menu == "Show All":
                st.subheader("Show All Purchase Records")
                try:
                    purchase_records = billing.show_all_purchase()
                    if purchase_records is not None:
                        columns = ["Purchase ID", "Supplier ID", "GSTIN Number", "Product ID", "Quantity", "Unit Price",
                                   "Total Price", "Discount", "CGST", "SGST", "IGST", "Amount", "Purchase Date", "Item Description"]
                        df = pd.DataFrame(purchase_records, columns=columns)
                        st.dataframe(df)
                except Exception as e:
                    st.error("Failed to fetch records from Purchase table: " + str(e))

            # Update Existing Purchase Record:
            elif billing_menu == "Update":
                st.subheader("Update Existing Purchase Record")
                purchase_id = st.number_input("Purchase ID", value=None, placeholder="Type a number...", step=1, key="purchase_id", help="Enter the unique numeric ID of the purchase record you want to update")
                supplier_id = st.number_input("Supplier ID", value=None, placeholder="Type a number...", step=1, key="supplier_id", help="Enter the updated numeric ID of the supplier")
                gstin_number = billing.get_gstin_number(supplier_id) if supplier_id else None
                gstin_number = st.text_input("GSTIN Number", value=gstin_number, key="gstin_number", help="Enter the updated GSTIN Number of the supplier")
                product_id = st.number_input("Product ID", value=None, placeholder="Type a number...", step=1, key="product_id", help="Enter the updated numeric ID of the product")
                quantity = st.number_input("Quantity", value=1, placeholder="Type a number...", step=1, key="quantity", help="Enter the updated quantity of the product purchased")
                product_price = billing.get_product_price(product_id) if product_id else None
                unit_price = st.number_input("Unit Price", value=product_price, key="unit_price", help="Enter the updated unit price of the product")
                tot_price = (quantity * unit_price) if quantity and unit_price else 0.0
                total_price = st.number_input("Total Price", value=tot_price, key="total_price", help="Calculate the updated total price of the purchase", disabled=True)
                discount = st.number_input("Discount", value=0.0, key="discount", help="Enter the updated discount amount")
                cgst = st.number_input("CGST", value=0.0, key="cgst", help="Enter the updated CGST amount")
                sgst = st.number_input("SGST", value=0.0, key="sgst", help="Enter the updated SGST amount")
                igst = st.number_input("IGST", value=0.0, key="igst", help="Enter the updated IGST amount")
                final_amount = (total_price - discount + cgst + sgst + igst)
                amount = st.number_input("Amount", value=final_amount, key="amount", help="Calculate the updated total amount of the purchase", disabled=True)
                purchase_date = st.date_input("Purchase Date", key="purchase_date", help="Select the updated date of the purchase")
                item = billing.get_item(product_id) if product_id else None
                item_description = st.text_area("Item", value=item, key="item", help="Enter the updated item description")
                if st.button("Update Purchase"):
                    try:
                        if validate_inputs(purchase_id, supplier_id, gstin_number, product_id, quantity, unit_price, total_price,
                                           discount, cgst, sgst, igst, amount, purchase_date, item_description):
                            billing.update_purchase(purchase_id, supplier_id, gstin_number,
                                                    product_id, quantity, unit_price,
                                                    total_price, discount, cgst, sgst,
                                                    igst, amount, purchase_date, item_description)
                    except Exception as e:
                        st.error("Failed to update record in Purchase table: " + str(e))

            # Delete Existing Purchase Record:
            elif billing_menu == "Delete":
                st.subheader("Delete Existing Purchase Record")
                purchase_id = st.number_input("Purchase ID", value=None, placeholder="Type a number...", step=1, key="purchase_id", help="Enter the unique numeric ID of the purchase record you want to delete")
                purchase_details = billing.purchase_details(purchase_id) if purchase_id else None
                if purchase_details is not None:
                    supplier_id = st.text_input("Supplier ID", value=purchase_details[1], key="supplier_id", disabled=True)
                    gstin_number = st.text_input("GSTIN Number", value=purchase_details[2], key="gstin_number", disabled=True)
                    product_id = st.text_input("Product ID", value=purchase_details[3], key="product_id", disabled=True)
                    quantity = st.text_input("Quantity", value=purchase_details[4], key="quantity", disabled=True)
                    unit_price = st.text_input("Unit Price", value=purchase_details[5], key="unit_price", disabled=True)
                    total_price = st.text_input("Total Price", value=purchase_details[6], key="total_price", disabled=True)
                    discount = st.text_input("Discount", value=purchase_details[7], key="discount", disabled=True)
                    cgst = st.text_input("CGST", value=purchase_details[8], key="cgst", disabled=True)
                    sgst = st.text_input("SGST", value=purchase_details[9], key="sgst", disabled=True)
                    igst = st.text_input("IGST", value=purchase_details[10], key="igst", disabled=True)
                    amount = st.text_input("Amount", value=purchase_details[11], key="amount", disabled=True)
                    purchase_date = st.text_input("Purchase Date", value=purchase_details[12], key="purchase_date", disabled=True)
                    item_description = st.text_area("Item", value=purchase_details[13], key="item", disabled=True)
                if st.button("Delete Purchase"):
                    try:
                        billing.delete_purchase(purchase_id)
                    except Exception as e:
                        st.error("Failed to delete record from Purchase table: " + str(e))

            # Close the database connection:
            # billing.connection.close()
            # st.info("Database connection closed successfully.")

        else:
            st.error("Failed to connect to the database.")

    except Exception as e:
        st.error("Failed to connect to the database: " + str(e))
