from .conn import HistoryConn
from .connector import ConnConnector
from .listeners import VerboseIQFeedListener
from .service import FeedService
from .exceptions import NoDataError, UnexpectedField, UnexpectedMessage
from .exceptions import UnexpectedProtocol, UnauthorizedError


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
        hist_conn = HistoryConn(name="dynamicasoft-historical-bars-for-trading")
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
                return bars
            except (NoDataError, UnauthorizedError) as err:
                print("No data returned because {0}".format(err))
                return False
