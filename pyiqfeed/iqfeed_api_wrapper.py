from .conn import HistoryConn
from .connector import ConnConnector
from .listeners import VerboseIQFeedListener
from .service import FeedService
from .exceptions import NoDataError, UnexpectedField, UnexpectedMessage
from .exceptions import UnexpectedProtocol, UnauthorizedError


import datetime as dt
import pytz


class IQFeedApiWrapper:
    def __init__(self, credentials):
        self.credentials = credentials
        self.launch_service()

    def launch_service(self):
        """Check if IQFeed.exe is running and start if not"""
        product, login, password = self.credentials
        svc = FeedService(product=product,
                          version="Debugging",
                          login=login,
                          password=password)
        svc.launch(headless=False)

    def get_last_n_bars(self, symbol: str, freq_in_sec: int, n: int, bar_unit: str = 's'):
        hist_conn = HistoryConn(
            name="dynamicasoft-historical-bars-for-trading")
        hist_listener = VerboseIQFeedListener("History Bar Listener")
        hist_conn.add_listener(hist_listener)

        with ConnConnector([hist_conn]) as connector:
            # look at conn.py for request_bars, request_bars_for_days and
            # request_bars_in_period for other ways to specify time periods etc
            try:
                bars = hist_conn.request_bars(ticker=symbol,
                                              interval_len=freq_in_sec,
                                              interval_type=bar_unit,
                                              max_bars=n)
                return bars.iloc[1:]
            except (NoDataError, UnauthorizedError) as err:
                print("No data returned because {0}".format(err))
                return False

    def get_candles_iqfeed(self, symbol: str, last_ts: int, freq_in_sec: int):
        now_ts = int(pytz.UTC.localize(
            dt.datetime.now(), is_dst=True).timestamp())
        expected_bars = int(((now_ts - last_ts) / freq_in_sec) + 0.5)
        bars = self.get_last_n_bars(symbol, freq_in_sec, expected_bars)
        if bars is False:
            return False

        def to_ts(datetime_str):
            tz = pytz.timezone('America/New_York')
            time = dt.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:00')
            time = tz.localize(time, is_dst=True)
            time = time.astimezone(pytz.utc)
            return int(time.timestamp())

        bars["tz-time"] = bars["datetime"].map(to_ts)
        return bars[bars["tz-time"] > last_ts]
