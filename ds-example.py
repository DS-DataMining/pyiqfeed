from pyiqfeed import IQFeedApiWrapper as IQFeedApiWrapper
from passwords import dtn_product_id, dtn_login, dtn_password


api = IQFeedApiWrapper((dtn_product_id, dtn_login, dtn_password))
df = api.get_last_n_bars(symbol="XG#", freq_in_sec=60, n=10)
print(df)
df = api.get_candles_iqfeed(symbol="XG#", freq_in_sec=60, last_ts=1563965400)
print(df)
