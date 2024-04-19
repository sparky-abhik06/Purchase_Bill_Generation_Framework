# Billing Management System
* **_First_**, you need to install the required packages by running the following command:
  ```bash
  pip install -r requirements.txt
  ```
* **_Second_**, you need to create a postgres database and create 3 tables:
  * **Supplier**
    ```sql
      CREATE TABLE Supplier (
          supplier_id INTEGER PRIMARY KEY,
          supplier_name VARCHAR(100) NOT NULL,
          landline_no VARCHAR(20),
          email VARCHAR(100) NOT NULL,
          mobile_no VARCHAR(20) NOT NULL,
          address TEXT NOT NULL,
          city VARCHAR(50) NOT NULL,
          state_province VARCHAR(50) NOT NULL,
          country VARCHAR(50) NOT NULL,
          postal_code VARCHAR(20) NOT NULL,
          gstin_number VARCHAR(20) NOT NULL
      );
    ```
  * **Product**
    ```sql
      CREATE TABLE Product (
          product_id INTEGER PRIMARY KEY,
          product_name VARCHAR(100) NOT NULL,
          description TEXT NOT NULL,
          category VARCHAR(50) NOT NULL,
          supplier_id INTEGER NOT NULL,
          unit_price FLOAT NOT NULL,
          FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id)
      );
    ```
  * **Purchase**
    ```sql
        CREATE TABLE Purchase (
          purchase_id INTEGER PRIMARY KEY,
          supplier_id INTEGER NOT NULL,
          gstin_number VARCHAR(20) NOT NULL,
          product_id INTEGER NOT NULL,
          quantity INTEGER NOT NULL,
          unit_price FLOAT NOT NULL,
          total_price FLOAT NOT NULL,
          discount FLOAT NOT NULL,
          cgst FLOAT NOT NULL,
          sgst FLOAT NOT NULL,
          igst FLOAT NOT NULL,
          amount FLOAT NOT NULL,
          purchase_date DATE NOT NULL,
          item_description TEXT NOT NULL,
          FOREIGN KEY (supplier_id) REFERENCES Supplier(supplier_id),
          FOREIGN KEY (product_id) REFERENCES Product(product_id)
      );
    ```
* **_Third_**, you need to create a `.env` file in the root directory and add the following environment variables:
  ```env
  DATABASE_URL=postgres://<username>:<password>@localhost:5432/<database_name>
  ```