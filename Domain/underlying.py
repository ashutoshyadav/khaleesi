import logging
import math
from enum import Enum
import pandas as pd

from data.company_returns import returns as company_returns
from domain.yahooUnderlying import YahooUnderlying

logger = logging.getLogger(__name__)


class RollingMethod(Enum):
    SIMPLE = 'SIMPLE'
    EXPONENTIAL = 'EXPONENTIAL'


class Underlying:

    def __init__(self, undl_code):
        self.code = undl_code
        logger.info(f'Initializing underlying: {undl_code}')
        self.name = None
        self.sector = None
        self.bloomberg_code = None
        self.ric_code = None
        self.return_on_earnings = None
        self.return_on_capital_employed = None
        self.currency = None
        self.first_trade_date = None
        self.exchange_name = None
        self.timezone = None
        self._hist_price = None
        self.returns_data = None
        self.dates = None
        self.returns_data = company_returns
        self._base_folder_path = 'C:\\Users\\Ashutosh\\Documents\\Codes\\khaleesi'
        self._load_data()

    def _load_data(self):
        logger.info(f'Loading data')
        undl = YahooUnderlying(self.code)
        self._hist_price = undl.get_historical_price()
        self._hist_price = pd.DataFrame(self._hist_price).T
        del self._hist_price['date']
        self.dates = self._hist_price.index
        for i in range(len(self.dates) - 1, 0, -1):
            if self._hist_price.at[self.dates[i], 'close'] is None:
                if i != len(self.dates) - 1:
                    self._hist_price.at[self.dates[i], 'close'] = self._hist_price.at[self.dates[i + 1], 'close']
                else:
                    self._hist_price.at[self.dates[i], 'close'] = 0
            if self._hist_price.at[self.dates[i], 'open'] is None:
                if i != len(self.dates) - 1:
                    self._hist_price.at[self.dates[i], 'open'] = self._hist_price.at[self.dates[i + 1], 'open']
                else:
                    self._hist_price.at[self.dates[i], 'open'] = 0
        self._hist_price['daily_return'] = self._hist_price.close - self._hist_price.open
        self._hist_price = self._hist_price.sort_index(ascending=False)
        self.dates = self._hist_price.index
        self.name = undl.name
        self.currency = undl.currency
        self.timezone = undl.timezone
        self.first_trade_date = undl.first_trade_date
        self.exchange_name = undl.exchange_name
        logger.info("Underlying Initialization complete")

    def _get_simple_rolling_return(self, dates) -> float:
        data = self._hist_price.loc[dates, :]
        returns = pd.Series([(data.at[dates[i], 'close'] / data.at[dates[i+1], 'close']) - 1
                             for i in range(len(dates)-1)])
        return returns.mean()

    def _get_simple_rolling_return_intraday(self, dates) -> float:
        data = self._hist_price.loc[dates, :]
        returns = pd.Series([(data.at[dates[i], 'close'] / data.at[dates[i], 'open']) - 1 for i in range(len(dates))])
        return returns.mean()

    def _get_exponential_rolling_return(self, dates) -> float:
        data = self._hist_price.loc[dates, :]
        _return = (data.at[dates[-1], 'close'] - data.at[dates[-2], 'close']) / data.at[dates[-2], 'close']
        alpha = 2 / len(dates)
        for i in range(len(dates)-3, 0, -1):
            _return = (((data.at[dates[i], 'close'] - data.at[dates[i+1], 'close']) / data.at[dates[i+1], 'close'])
                       * alpha) + (_return * (1 - alpha))
        return _return

    def _get_exponential_rolling_return_intraday(self, dates) -> float:
        data = self._hist_price.loc[dates, :]
        _return = (data.loc[dates[-1], 'close'] - data.loc[dates[-1], 'open']) / data.loc[dates[-1], 'open']
        alpha = 2 / len(dates)
        for i in range(len(dates)-2, 0, -1):
            _return = (((data.loc[dates[i], 'close'] - data.loc[dates[i], 'open']) / data.loc[dates[i], 'open']) *
                       alpha) + (_return * (1 - alpha))
        return _return

    def get_rolling_return(self, days: int, method: RollingMethod = RollingMethod.SIMPLE) -> float:
        dates = self.dates[days]
        if method == RollingMethod.SIMPLE:
            return self._get_simple_rolling_return(dates)
        else:
            return self._get_exponential_rolling_return(dates)

    def get_rolling_return_intraday(self, days: int, method: RollingMethod = RollingMethod.SIMPLE):
        dates = self.dates[:days]
        if method == RollingMethod.SIMPLE:
            return self._get_simple_rolling_return_intraday(dates)
        else:
            return self._get_exponential_rolling_return_intraday(dates)

    def get_prev_closing_price(self):
        return self._hist_price.loc[self.dates[0], 'close']

    def get_closing_prices_from(self, start_date):
        dates = self.dates[: self.dates.get_loc(start_date)]
        return self._hist_price.loc[dates, 'close']

    def expected_return_intraday(self, start_date):
        dates = self.dates[: start_date]
        return self._hist_price.loc[dates, 'daily_return'].mean()

    def get_returns(self, start_date):
        prices = self.get_closing_prices_from(start_date)
        res = pd.Series(
            [(prices[i] / prices[i + 1]) - 1 for i in range(len(prices) - 1) if prices[i] and prices[i + 1]])
        return res

    def expected_return(self, start_date):
        prices = self.get_closing_prices_from(start_date)
        res = pd.Series([(prices[i] / prices[i+1]) - 1 for i in range(len(prices)-1) if prices[i] and prices[i+1]])
        return res.mean()

    def variance(self, start_date):
        prices = self.get_closing_prices_from(start_date)
        returns = pd.Series([(prices[i] / prices[i + 1]) - 1 for i in range(len(prices) - 1) if prices[i] and
                             prices[i+1]])
        returns2 = returns * returns
        return returns2.mean() - math.pow(returns.mean(), 2)
