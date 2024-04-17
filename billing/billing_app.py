import logging

from billing.billing_main import main_billing

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main_billing()
