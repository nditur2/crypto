import config as cfg
import PollingCrypto as pc
from DBUtil import DBManager


log = cfg.get_logger(__name__)


class CryptoService:
    polling_crypto = pc.PollingCrypto()

    def __init__(self):
        log.debug("init CryptoService")


    '''
    Trigger the pooling of get prices each 1 minutes
    '''
    def poll(self):
        log.debug("poll")
        #ToDo: Can give the interval as parameter
        CryptoService.polling_crypto.start_polling()
        return "PollingCrypto was started"


    '''
    Get all the pairs from the DB
    Return: List of pairs
    '''
    def get_pairs(self):
        log.debug("get_pairs")
        db_manager = DBManager()
        get_distinct_pairs = db_manager.get_distinct_pairs()
        db_manager.close_connection()

        return get_distinct_pairs



    '''
    Get the given metric prices from the last hours
    params:
    metrics to get the prices of
    last_hours to get the prices of. Default: 24 hours
    
    Return: list of [price_date,price,metric,market]
    '''
    def get_last_metric_prices(self, metric: str, last_hours: int = 24):
        log.debug("get_last_metric_prices")
        db_manager = DBManager()
        last_metric_prices = db_manager.get_last_metric_prices(metric, last_hours)
        db_manager.close_connection()

        return last_metric_prices


    '''
    Calculate the rank of each metric in the last given last_hour.
    params:
    last_hours to calculate the rank of. Default: 24 hours
    
    Return: list of [metric,rank]
    '''
    def get_ranks(self, last_hours: int = 24):
        log.debug("get_ranks")
        db_manager = DBManager()
        last_metric_std = db_manager.get_std(last_hours)
        db_manager.close_connection()

        # Calculate the rank
        last_metric_std['rank'] = last_metric_std['row_index'] / last_metric_std.shape[0]
        log.debug(f"last_metric_std: {last_metric_std.head(10)}")

        # Actually we don't need the std and the row_index itself in the rank_df
        rank_df = last_metric_std[['pair', 'rank']]
        return rank_df.values.tolist()

