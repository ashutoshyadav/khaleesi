import logging
from enum import Enum

from scipy.optimize import minimize

from data.indice import ALLUNDERLYINGS
from domain.underlying import Underlying
import pandas as pd
import numpy as np


logger = logging.getLogger(__name__)


class Sector(Enum):
    FINANCIAL = 'FINANCIAL'
    NON_FINANCIAL = 'NON-FINANCIAL'


class Suggestor:

    def __init__(self):
        self.underlyings = [Underlying(undl_code) for undl_code in ALLUNDERLYINGS]
        self.selected_underlyings = None
        self.start_date = None
        self.risk_free_return = 0.0
        self.lower_bound = 0
        self.upper_bound = 1
        self.precision = 0.000000000001

    def set_lower_bound(self, val):
        self.lower_bound = val

    def set_upper_bound(self, val):
        self.upper_bound = val

    def reset_selection(self):
        self.selected_underlyings = None

    def select(self, cnt: int, sector: Sector):
        selected_underlyings = []
        for undl in self.underlyings:
            if Sector(undl.sector) == sector:
                if len(selected_underlyings) < cnt:
                    selected_underlyings.append(undl)
                else:

                    selected_underlyings.sort(key=lambda x: x.return_on_earnings if sector == Sector.FINANCIAL
                                              else x.return_on_capital_employed)
                    if sector == Sector.FINANCIAL and \
                            selected_underlyings[0].return_on_earnings < undl.return_on_earnings:
                        selected_underlyings[0] = undl
                    elif sector == Sector.NON_FINANCIAL and \
                            selected_underlyings[0].return_on_capital_employed < undl.return_on_capital_employed:
                        selected_underlyings[0] = undl
        if not self.selected_underlyings:
            self.selected_underlyings = []
        self.selected_underlyings.extend(selected_underlyings)
        self._update_start_date()

    def reset(self):
        self.selected_underlyings = None
        self.start_date = None
        self.risk_free_return = 0.0
        self.lower_bound = 0
        self.upper_bound = 1
        self.precision = 0.000000000001

    def _update_start_date(self):
        self.start_date = max([item.dates[-1] for item in self.selected_underlyings])

    @property
    def variance_vector(self):
        return pd.Series([item.variance(self.start_date) for item in self.selected_underlyings])

    @property
    def expected_return_vector(self):
        return pd.Series([item.expected_return(self.start_date) for item in self.selected_underlyings])

    @property
    def historical_returns_matrix(self):
        return [list(item.get_returns(self.start_date)) for item in self.selected_underlyings]

    @property
    def covariance_matrix(self):
        return np.cov(self.historical_returns_matrix)

    @property
    def correlation_matrix(self):
        return np.corrcoef(self.historical_returns_matrix)

    def save_returns_matrix_to_csv(self, path):
        returns_dict = {}
        for item in self.selected_underlyings:
            returns_dict[item.code] = item.get_returns(self.start_date).tolist()
        returns_mat = pd.DataFrame(returns_dict,
                                   index=pd.DatetimeIndex(
                                       self.selected_underlyings[0].dates[:self.selected_underlyings[0].dates.get_loc(
                                           self.start_date) - 1]), )
        returns_mat.to_csv(path, index=False)

    def calculate_portfolio_variance(self, weights):
        res = np.dot(np.dot(weights, self.covariance_matrix), weights.T)
        return res

    @staticmethod
    def _constraint(weights):
        return weights.sum() - 1

    def calculate_risk_contribution(self, weights):
        sigma = np.sqrt(self.calculate_portfolio_variance(weights))
        # Marginal Risk Contribution
        mrc = (weights * self.covariance_matrix) / sigma
        # Risk Contribution
        return np.multiply(mrc, weights.T)

    def equal_risk_objective(self, weights):
        x_t = pd.Series([1 for _ in range(len(self.selected_underlyings))])  # risk target in percent of portfolio risk
        x_t = x_t / x_t.sum()
        sig_p = np.sqrt(self.calculate_portfolio_variance(weights))  # portfolio sigma
        risk_target = np.asmatrix(np.multiply(sig_p, x_t))
        asset_rc = self.calculate_risk_contribution(weights)
        res = (np.square(asset_rc - risk_target.T)).sum()  # sum of squared error
        return res

    def get_equal_risk_portfolio(self):
        logger.info('Solving for equal risk')
        weights = pd.Series([np.random.normal() for _ in range(len(self.selected_underlyings))])
        weights = weights / weights.sum()
        weights = minimize(self.equal_risk_objective,
                           weights,
                           bounds=[(self.lower_bound, self.upper_bound) for _ in range(len(self.selected_underlyings))],
                           constraints={
                               'type': 'eq',
                               'fun': self._constraint
                           },
                           options={'disp': True},
                           tol=self.precision)
        logger.info(weights.message)
        return weights.x

    def get_minimum_variance_portfolio(self):
        logger.info('Solving for Minimum Variance')
        weights = pd.Series([np.random.normal() for _ in range(len(self.variance_vector))])
        weights = weights / weights.sum()
        weights = minimize(self.calculate_portfolio_variance,
                           weights,
                           bounds=[(self.lower_bound, self.upper_bound) for _ in range(len(self.variance_vector))],
                           constraints={
                               'type': 'eq',
                               'fun': self._constraint
                           },
                           tol=self.precision)
        logger.debug(weights.message)
        return weights.x

    def get_sharpe_ratio(self, weights):
        res = weights * self.expected_return_vector
        res = res.sum() - self.risk_free_return
        var = np.dot(np.dot(pd.Series(weights), self.covariance_matrix), pd.Series(weights).T)
        sd = np.math.sqrt(var)
        res = res / sd
        return res

    def _negate_sharpe_ratio(self, weights):
        return -1 * self.get_sharpe_ratio(weights)

    def get_maximum_shape_ratio_portfolio(self):
        logger.info('Solving for maximum Sharpe Ratio')
        weights = pd.Series([np.random.normal() for _ in range(len(self.variance_vector))])
        weights = weights / weights.sum()
        weights = minimize(self._negate_sharpe_ratio,
                           weights,
                           bounds=[(self.lower_bound, self.upper_bound) for _ in range(len(self.variance_vector))],
                           constraints={
                               'type': 'eq',
                               'fun': self._constraint
                           },
                           tol=self.precision)
        logger.debug(weights.message)
        return weights.x
