import config as cfg
from DBUtil import DBManager
import threading
from time import sleep
import pandas as pd
import requests


log = cfg.get_logger(__name__)


class PollingCrypto:
    # ToDo: Set this in a setting.yaml file
    prices_url = "https://api.cryptowat.ch/markets/prices"
    polling_started = False

    def __init__(self):
        log.debug("PollingCrypto init")

    def start_polling(self):
        if PollingCrypto.polling_started == False:
            threading.Timer(1, self.polling).start()
            PollingCrypto.polling_started = True

    #ToDo: Add stop_polling method

    def polling(self, interval_in_sec=60):
        log.debug("polling")
        while True:
            self.get_prices()
            sleep(interval_in_sec)

    '''
    Send GET prices HTTP request and save the results in the 'prices' table with current time
    '''
    def get_prices(self):
        log.debug("get_prices")
        #ToDo: Handle paginated response here
        response = requests.get(self.prices_url)
        #ToDo: handle errors
        prices_json_result = response.json()["result"];
        df = pd.DataFrame(prices_json_result.items(), columns=['type_market_pair','price'])
        #extract results into columns
        df[['type', 'market', 'pair']] = df['type_market_pair'].str.split(':', expand=True)

        #filter out non market results
        filtered_prices_df = df[df['type']=="market"]
        log.info(f"filtered_prices_df: {filtered_prices_df.head(10)}")

        # Save the prices in the DB
        db_manager = DBManager()
        db_manager.add_new_prices(filtered_prices_df)
        db_manager.close_connection()

