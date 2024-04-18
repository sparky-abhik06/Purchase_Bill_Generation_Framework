import re
import pandas as pd
import streamlit as st
import psycopg2
import logging

from database_connection.database_connection import DatabaseConnection


# Validating User Inputs:
def validate_inputs(supplier_id: int, supplier_name: str, landline_no: str, email: str, country_code: str,
                    mobile_no: str,
                    address: str, city: str, state_province: str, country: str, postal_code: str, gstin_number: str):
    if not supplier_id or supplier_id <= 0:
        st.warning("Please enter the Supplier ID")
        return False
    if not supplier_name.strip():
        st.warning("Please enter the Supplier Name")
        return False
    if not landline_no.strip():
        st.warning("Please enter the Landline Number")
        return False
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        st.warning("Please enter a valid Email Address")
        return False
    if not country_code.strip():
        st.warning("Please enter the Country Code")
        return False
    if not mobile_no.strip():
        st.warning("Please enter the Mobile Number")
        return False
    if not address.strip():
        st.warning("Please enter the Address")
        return False
    if not city.strip():
        st.warning("Please enter the City")
        return False
    if not state_province.strip():
        st.warning("Please enter the State/Province")
        return False
    if not country.strip():
        st.warning("Please enter the Country")
        return False
    if not postal_code.strip():
        st.warning("Please enter the Postal Code")
        return False
    if not gstin_number.strip():
        st.warning("Please enter the GSTIN Number")
        return False
    else:
        return True


# Creating Supplier Class:
class Supplier:
    def __init__(self, connection):
        self.connection = connection

    def insert_supplier(self, supplier_id: int, supplier_name: str, landline_no: str, email: str, mobile_no: str,
                        address: str, city: str, state_province: str, country: str, postal_code: str,
                        gstin_number: str):
        try:
            cursor = self.connection.cursor()
            postgres_insert_query = """INSERT INTO Supplier (supplier_id, supplier_name, landline_no, email, country_code, mobile_no, address, city, state_province, country, postal_code, gstin_number) VALUES (%x,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            record_to_insert = (supplier_id, supplier_name, landline_no, email, mobile_no, address, city,
                                state_province, country, postal_code, gstin_number)
            cursor.execute(postgres_insert_query, record_to_insert)
            self.connection.commit()
            count = cursor.rowcount
            st.success(f"{count} Record(s) inserted successfully into Supplier table")
        except (Exception, psycopg2.Error) as error:
            st.error("Failed to insert record into Supplier table: " + str(error))

    def update_supplier(self, supplier_id: int, supplier_name: str, landline_no: str, email: str, mobile_no: str,
                        address: str, city: str, state_province: str, country: str, postal_code: int,
                        gstin_number: str):
        try:
            cursor = self.connection.cursor()
            postgres_update_query = """UPDATE Supplier SET supplier_name = %s, landline_no = %s, email = %s, country_code = %s, mobile_no = %s, address = %s, city = %s, state_province = %s, country = %s, postal_code = %s, gstin_number = %s WHERE supplier_id = %x"""
            record_to_update = (supplier_name, landline_no, email, mobile_no, address, city, state_province,
                                country, postal_code, gstin_number, supplier_id)
            cursor.execute(postgres_update_query, record_to_update)
            self.connection.commit()
            count = cursor.rowcount
            st.success(f"{count} Record(s) updated successfully in Supplier table")
        except (Exception, psycopg2.Error) as error:
            st.error("Failed to update record in Supplier table: " + str(error))

    def delete_supplier(self, supplier_id: int):
        try:
            cursor = self.connection.cursor()
            postgres_delete_query = """DELETE FROM Supplier WHERE supplier_id = %x"""
            cursor.execute(postgres_delete_query, (supplier_id,))
            self.connection.commit()
            count = cursor.rowcount
            st.success(f"{count} Record(s) deleted successfully from Supplier table")
        except (Exception, psycopg2.Error) as error:
            st.error("Failed to delete record from Supplier table: " + str(error))

    def show_all_suppliers(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""SELECT * FROM Supplier""")
            suppliers = cursor.fetchall()
            if len(suppliers) > 0:
                return suppliers
            else:
                st.info("No records found in the Supplier table")
                return None
        except (Exception, psycopg2.Error) as error:
            st.error("Failed to fetch records from Supplier table: " + str(error))
            return None

    def search_supplier(self, **kwargs):
        try:
            cursor = self.connection.cursor()
            query = """SELECT * FROM Supplier WHERE """
            conditions = []
            values = []
            for key, value in kwargs.items():
                if value is not None and value != "":
                    conditions.append(f"{key} = %s")
                    values.append(value)
            query += " AND ".join(conditions)
            cursor.execute(query, tuple(values))
            supplier = cursor.fetchall()
            if len(supplier) > 0:
                return supplier
            else:
                st.info("No supplier found with the given search criteria")
                return None
        except (Exception, psycopg2.Error) as error:
            st.error("Failed to fetch records from Supplier table: " + str(error))
            return None


# Streamlit UI for Supplier Management:
def main_supplier():
    st.header("Supplier Information Management")
    try:
        supplier = Supplier(DatabaseConnection("postgres", "postgres", "password", "localhost", "5432").connect())
        if supplier.connection is not None:
            supplier_menu = st.selectbox("Supplier Menu", ["Insert", "Show All", "Search", "Update", "Delete"],
                                         key="supplier_menu",
                                         help="Select the operation you want to perform on the Supplier table")

            # Insert New Supplier:
            if supplier_menu == "Insert":
                st.subheader("Insert New Supplier")
                supplier_id = int(
                    st.number_input("Supplier ID", value=None, placeholder="Type a number...", step=1,
                                    key="supplier_id", help="Enter the unique numeric ID for the new supplier"))
                supplier_name = st.text_input("Supplier Name", key="supplier_name",
                                              help="Enter the name of the new supplier")
                landline_no = st.text_input("Landline Number", key="landline_no",
                                            help="Enter the landline number of the new supplier")
                email = st.text_input("Email", key="email", help="Enter the email address of the new supplier")
                country_code = st.text_input("Country Code", key="country_code",
                                             help="Enter the country code of the new supplier")
                mobile_no = st.text_input("Mobile Number", key="mobile_no",
                                          help="Enter the mobile number of the new supplier")
                address = st.text_input("Address", key="address", help="Enter the address of the new supplier")
                city = st.text_input("City", key="city", help="Enter the city of the new supplier")
                state_province = st.text_input("State/Province", key="state_province",
                                               help="Enter the state/province of the new supplier")
                country = st.text_input("Country", key="country", help="Enter the country of the new supplier")
                postal_code = st.text_input("Postal Code", key="postal_code",
                                            help="Enter the postal code of the new supplier")
                gstin_number = st.text_input("GSTIN Number", key="gstin_number",
                                             help="Enter the GSTIN number of the new supplier")
                if st.button("Insert", key="insert"):
                    try:
                        if validate_inputs(supplier_id, supplier_name, landline_no, email, country_code, mobile_no,
                                           address, city, state_province, country, postal_code, gstin_number):
                            supplier.insert_supplier(supplier_id=supplier_id, supplier_name=supplier_name,
                                                     landline_no=landline_no, email=email, mobile_no=mobile_no,
                                                     address=address, city=city, state_province=state_province,
                                                     country=country, postal_code=postal_code,
                                                     gstin_number=gstin_number)
                    except Exception as e:
                        st.error("An error occurred while inserting the record: " + str(e))

            # Show All Suppliers:
            elif supplier_menu == "Show All":
                st.subheader("All Suppliers")
                try:
                    suppliers = supplier.show_all_suppliers()
                    if suppliers is not None:
                        columns = ["Supplier ID", "Supplier Name", "Landline Number", "Email", "Mobile Number",
                                   "Address", "City", "State/Province", "Country", "Postal Code", "GSTIN Number"]
                        df = pd.DataFrame(suppliers, columns=columns)
                        st.dataframe(df)
                except Exception as e:
                    st.error("An error occurred while fetching the records: " + str(e))

            # Search Supplier:
            elif supplier_menu == "Search":
                st.subheader("Search Supplier")
                supplier_id = int(
                    st.number_input("Supplier ID", value=None, placeholder="Type a number...", step=1,
                                    key="supplier_id",
                                    help="Enter the unique numeric ID of the supplier to be searched"))
                supplier_name = st.text_input("Supplier Name", key="supplier_name",
                                              help="Enter the name of the supplier to be searched")
                city = st.text_input("City", key="city", help="Enter the city of the supplier to be searched")
                state_province = st.text_input("State/Province", key="state_province",
                                               help="Enter the state/province of the supplier to be searched")
                country = st.text_input("Country", key="country",
                                        help="Enter the country of the supplier to be searched")
                gstin_number = st.text_input("GSTIN Number", key="gstin_number",
                                             help="Enter the GSTIN number of the supplier to be searched")
                if st.button("Search", key="search"):
                    try:
                        suppliers = supplier.search_supplier(supplier_id=supplier_id if supplier_id else None,
                                                             supplier_name=supplier_name if supplier_name else None,
                                                             city=city if city else None,
                                                             state_province=state_province if state_province else None,
                                                             country=country if country else None,
                                                             gstin_number=gstin_number if gstin_number else None)
                        if suppliers is not None:
                            columns = ["Supplier ID", "Supplier Name", "Landline Number", "Email", "Mobile Number",
                                       "Address", "City", "State/Province", "Country", "Postal Code", "GSTIN Number"]
                            df = pd.DataFrame(suppliers, columns=columns)
                            st.dataframe(df)
                        else:
                            st.warning("No supplier found with the given search criteria")
                    except Exception as e:
                        st.error("An error occurred while searching the records: " + str(e))

            # Update Existing Supplier:
            elif supplier_menu == "Update":
                st.subheader("Update Existing Supplier")
                supplier_id = int(
                    st.number_input("Supplier ID", value=None, placeholder="Type a number...", step=1,
                                    key="supplier_id",
                                    help="Enter the unique numeric ID of the supplier to be updated"))
                supplier_name = st.text_input("Supplier Name", key="supplier_name",
                                              help="Enter the updated name of the supplier")
                landline_no = st.text_input("Landline Number", key="landline_no",
                                            help="Enter the updated landline number of the supplier")
                email = st.text_input("Email", key="email", help="Enter the updated email address of the supplier")
                country_code = st.text_input("Country Code", key="country_code",
                                             help="Enter the updated country code of the supplier")
                mobile_no = st.text_input("Mobile Number", key="mobile_no",
                                          help="Enter the updated mobile number of the supplier")
                address = st.text_input("Address", key="address", help="Enter the updated address of the supplier")
                city = st.text_input("City", key="city", help="Enter the updated city of the supplier")
                state_province = st.text_input("State/Province", key="state_province",
                                               help="Enter the updated state/province of the supplier")
                country = st.text_input("Country", key="country", help="Enter the updated country of the supplier")
                postal_code = st.text_input("Postal Code", key="postal_code",
                                            help="Enter the updated postal code of the supplier")
                gstin_number = st.text_input("GSTIN Number", key="gstin_number",
                                             help="Enter the updated GSTIN number of the supplier")
                if st.button("Update", key="update"):
                    try:
                        if validate_inputs(supplier_id, supplier_name, landline_no, email, country_code, mobile_no,
                                           address, city, state_province, country, postal_code, gstin_number):
                            supplier.update_supplier(supplier_id=supplier_id, supplier_name=supplier_name,
                                                     landline_no=landline_no, email=email, mobile_no=mobile_no,
                                                     address=address, city=city, state_province=state_province,
                                                     country=country, postal_code=postal_code,
                                                     gstin_number=gstin_number)
                    except Exception as e:
                        st.error("An error occurred while updating the record: " + str(e))

            # Delete Existing Supplier:
            elif supplier_menu == "Delete":
                st.subheader("Delete Existing Supplier")
                supplier_id = int(
                    st.number_input("Supplier ID", value=None, placeholder="Type a number...", step=1,
                                    key="supplier_id",
                                    help="Enter the unique numeric ID of the supplier to be deleted"))
                if st.button("Delete", key="delete"):
                    try:
                        supplier.delete_supplier(supplier_id)
                    except Exception as e:
                        st.error("An error occurred while deleting the record: " + str(e))

            # Close the database connection:
            supplier.connection.close()
            st.info("Database connection closed successfully.")

        else:
            st.error("An error occurred while connecting to the database.")

    except Exception as e:
        st.error("An error occurred while connecting to the database: " + str(e))
