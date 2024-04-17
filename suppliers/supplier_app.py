import logging

from suppliers.supplier_main import main_supplier

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main_supplier()
