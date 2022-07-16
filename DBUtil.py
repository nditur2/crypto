import pymysql
from sqlalchemy import create_engine
import config as cfg
import datetime as dt
import pandas as pd


log = cfg.get_logger(__name__)

class DBManager:

    #ToDo: Use AWS SECRET for getting this information
    #ToDo: Fill the details here
    host = "XXX"
    user="XXX"
    password="XXX"
    database="XXX"
    port="3306"

    TABLE = "prices"

    '''
    Open connection to the DB
    '''
    def __init__(self):
        #ToDo: Consider open connection per request and close it immediately after the request
        self.connection = pymysql.connect(host=self.host,user=self.user,password=self.password,db=self.database)
        self.cursor = self.connection.cursor()
        self.engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                               .format(user=self.user,
                                       pw=self.password,
                                       host=self.host,
                                       db=self.database))


    '''
    Close the connection to the DB
    '''
    def close_connection(self):
        log.debug("close_connection")
        if self.connection is not None:
            self.connection.close()


    '''
    Get pandas data frame and save in the DB with current date taime column
    params: 
    prices_df: data grame with 'market', 'pair', 'price' columns.
    '''
    def add_new_prices(self, prices_df: pd.DataFrame):
        log.debug("adding new prices")
        prices_df = prices_df[['market', 'pair', 'price']]
        #adding current time as the price time
        prices_df['price_date'] = dt.datetime.now()
        #Save in the DB
        #ToDo: handle errors
        prices_df.to_sql(self.TABLE, con=self.engine, if_exists='append', chunksize=1000)


    '''
    Get all the pairs in the DB.
    '''
    def get_distinct_pairs(self):
        #ToDo: handle errors
        #ToDo: Consider getting only the pairs with data from the last X hours
        self.cursor.execute(f"SELECT distinct pair from {self.TABLE}")
        distinc_pairs = self.cursor.fetchall()
        #Flat the list of lists into list
        flat_distinc_pairs = [pair for pair_list in distinc_pairs for pair in pair_list]
        return flat_distinc_pairs


    '''
    Get the pricres of the given metric from the last given hours
    params:
    metric to get the prices of
    last_hours to get the prices of. Default: 24 hours
    '''
    def get_last_metric_prices(self, metric, last_hours=24):
        #ToDo: handle errors
        log.debug(f"metric: {metric}, last_hours: {last_hours}")
        till_time = self.__get_datetime_befor_x_hours(last_hours)

        self.cursor.execute(f"SELECT price_date,price,pair,market from {self.TABLE} WHERE pair = '{metric}' and price_Date >= '{till_time}'")
        last_metric_prices = self.cursor.fetchall()
        log.debug(f"last_metric_prices: {last_metric_prices}")
        #ToDo: handle the price format
        return last_metric_prices


    '''
    Calculate the std of the whole pair from the last given hours
    params:
    last_hours to calculate the std of
    
    return data frame with 'pair','std','row_index' columns
    '''
    def get_std(self, last_hours=24):
        #ToDo: handle errors
        log.debug(f"last_hours: {last_hours}")
        till_time = self.__get_datetime_befor_x_hours(last_hours)

        #ToDo: We calculate here the std all over the markets. Consider distinguish between markets
        #row_index is the nukber of the row while sorting by the std in DESC order
        self.cursor.execute(f"SELECT *, ROW_NUMBER() OVER(ORDER BY std DESC) as row_index FROM ( "
                            f"SELECT pair, STD(price) as std FROM {self.TABLE} " 
                            f" WHERE price_date >= '{till_time}' " 
                            f" GROUP BY pair) std_query")
        last_metrics_prices = self.cursor.fetchall()
        return pd.DataFrame(list(last_metrics_prices), columns=['pair','std','row_index'])



    def __get_datetime_befor_x_hours(self, last_hours):
        till_time = (dt.datetime.now() - dt.timedelta(hours=last_hours)).strftime("%Y-%m-%d %H:%M:%S")
        log.debug(f"till_time: {till_time}")
        return till_time



