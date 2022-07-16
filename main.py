import uvicorn
from fastapi import FastAPI
import config as cfg
import CryptoService as cs

log = cfg.get_logger(__name__)
app = FastAPI()
crypto_service = cs.CryptoService()


@app.get("/")
async def read_root():
    log.info("read_root")
    return "Hello crypto application!"


'''
This endpoint should be called once for triggering the polling.
It can be called for example by a lambda
'''
#ToDo: Ensure it doesn't call in parallel
@app.post("/poll")
async def poll():
    log.info("poll")
    return crypto_service.poll()


'''
This endpoint return all the pairs we have in the DB.
'''
@app.get("/pairs")
async def get_paris():
    log.info("get_paris")
    return crypto_service.get_pairs()


'''
This endpoint returns the price of the give metric in the last given last_hour.

params:
metric to get the prices of
last_hours to get the prices of. Default: 24 hours

Return: list of [price_date,price,metric,market]
'''
@app.get("/get_last_metric_prices")
async def get_last_metric_prices(metric: str, last_hours: int = 24):
    log.info(f"get_last_metric_prices: metric={metric}, last_hours={last_hours}")
    return crypto_service.get_last_metric_prices(metric,last_hours)


'''
This endpoint returns the rank of each metric in the last given last_hour.
params:
last_hours to calculate the rank of. Default: 24 hours

Return: list of [metric,rank]
'''
#ToDo: return in paging
@app.get("/get_ranks")
async def get_ranks(last_hours: int = 24):
    log.info(f"get_ranks: last_hours={last_hours}")
    return crypto_service.get_ranks(last_hours)




if __name__ == "__main__":
    log.info("main")
    uvicorn.run(app)


