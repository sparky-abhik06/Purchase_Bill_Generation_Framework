import pandas as pd
import streamlit as st
import psycopg2

from database_connection.database_connection import DatabaseConnection


# Validating User Inputs:
def validate_inputs(product_id: int, product_name: str, description: str, category: str, supplier_id: int,
                    unit_price: float):
    if not product_id:
        st.warning("Please enter the Product ID")
        return False
    if not product_name.strip():
        st.warning("Please enter the Product Name")
        return False
    if not description.strip():
        st.warning("Please enter the Description")
        return False
    if not category.strip():
        st.warning("Please enter the Category")
        return False
    if not supplier_id:
        st.warning("Please enter the Supplier ID")
        return False
    if not unit_price:
        st.warning("Please enter the Unit Price")
        return False
    else:
        return True

# Creating Product Class:
class Product:
    def __init__(self, connection):
        self.connection = connection

    def insert_product(self, product_id: int, product_name: str, description: str, category: str, supplier_id: int,
                       unit_price: float):
        try:
            cursor = self.connection.cursor()
            postgres_insert_query = """ INSERT INTO Product (product_id, product_name, description, category, supplier_id, price) VALUES (%x,%s,%s,%s,%x,%f)"""
            record_to_insert = (product_id, product_name, description, category, supplier_id, unit_price)
            cursor.execute(postgres_insert_query, record_to_insert)
            self.connection.commit()
            count = cursor.rowcount
            st.success(f"{count} Record(s) inserted successfully into Product table")
        except (Exception, psycopg2.Error) as error:
            st.error("Failed to insert record into Product table: " + str(error))

    def update_product(self, product_id: int, product_name: str, description: str, category: str, supplier_id: int,
                       unit_price: float):
        try:
            cursor = self.connection.cursor()
            postgres_update_query = """UPDATE Product SET product_name = %s, description = %s, category = %s, supplier_id = %x, price = %f WHERE product_id = %x"""
            record_to_update = (product_name, description, category, supplier_id, unit_price, product_id)
            cursor.execute(postgres_update_query, record_to_update)
            self.connection.commit()
            count = cursor.rowcount
            st.success(f"{count} Record(s) updated successfully in Product table")
        except (Exception, psycopg2.Error) as error:
            st.error("Failed to update record in Product table: " + str(error))

    def delete_product(self, product_id: int):
        try:
            cursor = self.connection.cursor()
            postgres_delete_query = """DELETE FROM Product WHERE product_id = %x"""
            cursor.execute(postgres_delete_query, (product_id,))
            self.connection.commit()
            count = cursor.rowcount
            st.success(f"{count} Record(s) deleted successfully from Product table")
        except (Exception, psycopg2.Error) as error:
            st.error("Failed to delete record from Product table: " + str(error))

    def show_all_products(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""SELECT * FROM Product""")
            products = cursor.fetchall()
            if len(products) > 0:
                return products
            else:
                st.info("No records found in the Product table")
                return None
        except (Exception, psycopg2.Error) as error:
            st.error("Failed to fetch records from Product table: " + str(error))

    def search_product(self, **kwargs):
        try:
            cursor = self.connection.cursor()
            search_query = """SELECT * FROM Product WHERE """
            conditions = []
            values = []
            for key, value in kwargs.items():
                if value is not None and value != "":
                    conditions.append(f"{key} = %s")
                    values.append(value)
            search_query += " AND ".join(conditions)
            cursor.execute(search_query, tuple(values))
            products = cursor.fetchall()
            if len(products) > 0:
                return products
            else:
                st.info("No records found in the Product table")
                return None
        except (Exception, psycopg2.Error) as error:
            st.error("Failed to fetch records from Product table: " + str(error))


# Streamlit UI for Product Management:
def main_product():
    st.header("Product Information Management")
    try:
        product = Product(DatabaseConnection("postgres", "postgres", "password", "localhost", "5432").connect())
        if product.connection is not None:
            product_menu = st.selectbox("Product Menu", ["Insert", "Show All", "Search", "Update", "Delete"], key="product_menu", help="Select the operation you want to perform on the Product table")

            # Insert New Product:
            if product_menu == "Insert":
                st.subheader("Insert New Product")
                product_id = st.number_input("Product ID", key="product_id", help="Enter the unique numeric ID for the new product")
                product_name = st.text_input("Product Name", key="product_name", help="Enter the name of the new product")
                description = st.text_area("Description", key="description", help="Enter the description of the new product")
                category = st.text_input("Category", key="category", help="Enter the category of the new product")
                supplier_id = st.number_input("Supplier ID", key="supplier_id", help="Enter the unique numeric ID of the supplier")
                unit_price = st.number_input("Unit Price", key="unit_price", help="Enter the unit price of the new product")
                if st.button("Insert Product"):
                    try:
                        if validate_inputs(product_id, product_name, description, category, supplier_id, unit_price):
                            product.insert_product(product_id=product_id, product_name=product_name, description=description,
                                                   category=category, supplier_id=supplier_id, unit_price=unit_price)
                    except Exception as e:
                        st.error("Failed to insert record into Product table: " + str(e))

            # Show All Products:
            elif product_menu == "Show All":
                st.subheader("Show All Products")
                try:
                    products = product.show_all_products()
                    if products is not None:
                        columns = ["Product ID", "Product Name", "Description", "Category", "Supplier ID", "Unit Price"]
                        df = pd.DataFrame(products, columns=columns)
                        st.dataframe(df)
                except Exception as e:
                    st.error("Failed to fetch records from Product table: " + str(e))

            # Search Product:
            elif product_menu == "Search":
                st.subheader("Search Product")
                product_id = st.number_input("Product ID", key="product_id", help="Enter the unique numeric ID of the product you want to search")
                product_name = st.text_input("Product Name", key="product_name", help="Enter the name of the product you want to search")
                category = st.text_input("Category", key="category", help="Enter the category of the product you want to search")
                supplier_id = st.number_input("Supplier ID", key="supplier_id", help="Enter the unique numeric ID of the supplier you want to search")
                if st.button("Search", key="search"):
                    try:
                        products = product.search_product(product_id=product_id if product_id else None,
                                                          product_name=product_name if product_name else None,
                                                          category=category if category else None,
                                                          supplier_id=supplier_id if supplier_id else None)
                        if products is not None:
                            columns = ["Product ID", "Product Name", "Description", "Category", "Supplier ID", "Unit Price"]
                            df = pd.DataFrame(products, columns=columns)
                            st.dataframe(df)
                    except Exception as e:
                        st.error("Failed to fetch records from Product table: " + str(e))

            # Update Existing Product:
            elif product_menu == "Update":
                st.subheader("Update Existing Product")
                product_id = st.number_input("Product ID", key="product_id", help="Enter the unique numeric ID of the product you want to update")
                product_name = st.text_input("Product Name", key="product_name", help="Enter the updated name of the product")
                description = st.text_area("Description", key="description", help="Enter the updated description of the product")
                category = st.text_input("Category", key="category", help="Enter the updated category of the product")
                supplier_id = st.number_input("Supplier ID", key="supplier_id", help="Enter the updated unique numeric ID of the supplier")
                unit_price = st.number_input("Unit Price", key="unit_price", help="Enter the updated unit price of the product")
                if st.button("Update Product"):
                    try:
                        if validate_inputs(product_id, product_name, description, category, supplier_id, unit_price):
                            product.update_product(product_id=product_id, product_name=product_name, description=description,
                                                   category=category, supplier_id=supplier_id, unit_price=unit_price)
                    except Exception as e:
                        st.error("Failed to update record in Product table: " + str(e))

            # Delete Existing Product:
            elif product_menu == "Delete":
                st.subheader("Delete Existing Product")
                product_id = st.number_input("Product ID", key="product_id", help="Enter the unique numeric ID of the product you want to delete")
                if st.button("Delete Product"):
                    try:
                        product.delete_product(product_id)
                    except Exception as e:
                        st.error("Failed to delete record from Product table: " + str(e))

            # Close the database connection:
            product.connection.close()
            st.info("Database connection closed successfully.")

        else:
            st.error("Failed to connect to the database.")

    except Exception as e:
        st.error("Failed to connect to the database: " + str(e))
