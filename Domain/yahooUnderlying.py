import json
import logging
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from enum import Enum


logger = logging.getLogger(__name__)


class Intervals(Enum):
    OneMin = '1m'
    TwoMin = '2m'
    FiveMin = '5m'
    FifteenMin = '15m'
    ThirtyMin = '30m'
    OneHour = '1h'
    NinetyMin = '90m'
    SixtyMin = '60m'
    OneDay = '1d'
    FiveDay = '5d'
    OneWeek = '1wk'
    OneMonth = '1mo'
    ThreeMonth = '3mo'


class Range(Enum):
    OneDay = '1d'
    FiveDay = '5d'
    OneMonth = '1mo'
    ThreeMonth = '3mo'
    SixMonth = '6mo'
    OneYear = '1y'
    TwoYear = '2y'
    FiveYear = '5y'
    TenYear = '10y'
    Max = 'max'
    YearToDate = 'ytd'


class YahooUnderlying:

    def __init__(self, undl_code):
        self.code = undl_code
        logger.info(f'Initializing Underlying with code: {undl_code}')
        self._name = None
        self._time_zone = None
        self._first_trade_date = None
        self._currency = None
        self._exchangeName = None
        self._instrument_type = None
        self._baseurl = f'https://query1.finance.yahoo.com/v8/finance/chart/{self.code}?'

    @property
    def name(self):
        if not self._name:
            self._fetch_data(data_range=Range.OneDay, interval=Intervals.OneHour)
        return self._name

    @property
    def exchange_name(self):
        if not self._exchangeName:
            self._fetch_data(data_range=Range.OneDay, interval=Intervals.OneHour)
        return self._exchangeName

    @property
    def insturment_type(self):
        if not self._instrument_type:
            self._fetch_data(data_range=Range.OneDay, interval=Intervals.OneHour)
        return self._instrument_type

    @property
    def currency(self):
        if not self._currency:
            self._fetch_data(data_range=Range.OneDay, interval=Intervals.OneHour)
        return self._currency

    @property
    def first_trade_date(self):
        if not self._first_trade_date:
            self._fetch_data(data_range=Range.OneDay, interval=Intervals.OneHour)
        return self._first_trade_date

    @property
    def timezone(self):
        if not self._time_zone:
            self._fetch_data(data_range=Range.OneDay, interval=Intervals.OneHour)
        return self._time_zone

    def get_current_price(self):
        data = self._fetch_data(data_range=Range.OneDay, interval=Intervals.OneMin)
        latest_key = sorted(data.keys(), reverse=True)[0]
        return data.get(latest_key).get('close')

    def get_historical_price_between_dates(self, start_date: datetime, end_date: datetime, interval: Intervals,
                                           data_range: Range):
        data = self._fetch_data(data_range=data_range, interval=interval)
        result = {}
        date = start_date
        while date <= end_date:
            result[date.strftime('%Y-%m-%d %H:%M:%S')] = data.get(date.strftime('%Y-%m-%d %H:%M:%S'))
            date = date + timedelta(days=1)
        return result

    def get_historical_price(self, data_range: Range = Range.TenYear, interval: Intervals = Intervals.OneDay):
        return self._fetch_data(data_range, interval)

    def _fetch_data(self, data_range: Range, interval: Intervals):
        response = None
        try:
            url = self._baseurl + urllib.parse.urlencode({
                'range': data_range.value,
                'interval': interval.value,
            })
            result = {}
            logger.info(f'calling url: {url}')
            response = urllib.request.urlopen(url)
            if response.status == 200:
                logger.info('Successful request response!')
                logger.info('Initializing underlying data')
                data = json.loads(response.read())
                for i in range(len(data.get('chart').get('result')[0].get('timestamp'))):
                    result[datetime.fromtimestamp(data.get('chart').get('result')[0]
                                                      .get('timestamp')[i]).strftime('%Y-%m-%d %H:%M:%S')] = {
                        'open': data.get('chart').get('result')[0]
                                    .get('indicators').get('quote')[0].get('open')[i],
                        'low': data.get('chart').get('result')[0]
                                    .get('indicators').get('quote')[0].get('low')[i],
                        'high': data.get('chart').get('result')[0]
                                    .get('indicators').get('quote')[0].get('high')[i],
                        'volume': data.get('chart').get('result')[0]
                                    .get('indicators').get('quote')[0].get('volume')[i],
                        'close': data.get('chart').get('result')[0]
                                    .get('indicators').get('quote')[0].get('close')[i],
                        'date': datetime.fromtimestamp(data.get('chart').get('result')[0]
                                                           .get('timestamp')[i]).strftime('%Y-%m-%d %H:%M:%S')
                    }

                self._exchangeName = self._exchangeName or data.get('chart').get('result')[0].get('meta')\
                                                               .get('exchangeName')
                self._currency = self._currency or data.get('chart').get('result')[0].get('meta').get('currency')
                self._instrument_type = self._instrument_type or data.get('chart').get('result')[0].get('meta')\
                                                                     .get('instrumentType')
                self._first_trade_date = self._first_trade_date or datetime.fromtimestamp(data.get('chart')
                                                                                              .get('result')[0]
                                                                                              .get('meta')
                                                                                              .get('firstTradeDate'))\
                    .strftime('%Y-%m-%d')
                self._time_zone = self._time_zone or data.get('chart').get('result')[0].get('meta').get('timezone')

            logger.info(f'Underlying data initialization complete for code: {self.code}')
            return result
        except Exception as e:
            logger.error(e)
            if response:
                raise RuntimeError(response.read())
            else:
                raise e
