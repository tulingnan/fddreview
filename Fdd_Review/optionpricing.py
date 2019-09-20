# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 18:30:26 2019

@author: TLN
"""
import numpy as np
from scipy.stats.mstats import gmean
from scipy.stats import norm
from scipy.sparse import coo_matrix
from numpy.linalg import inv


class OptionPricing(object):
    def __init__(self, S, K):
        self.S = stock_Price
        self.K = strike_Price

    def BlackSholes(self, t, maturity_date, interest_rate,
                    dividend_yield, volatility, flag):
        dt = maturity_date - t
        y_discount = np.exp(-dividend_yield * dt)
        d1 = ((np.log(self.stock_price / self.strike_price1) + (interest_rate -
                                                                dividend_yield + 0.5 * volatility ** 2) * dt)
              / (volatility * np.sqrt(dt)))
        d2 = d1 - volatility * np.sqrt(dt)
        if flag == 'call':
            bs_european_call_price = (self.stock_price * y_discount * norm.cdf(d1) -
                                      self.strike_price1 * discount * norm.cdf(d2))
            bs_european_call_delta = y_discount * norm.cdf(d1)
            bs_european_call_theta = (- (self.stock_price * norm.pdf(d1) * volatility
                                         * y_discount) / (2 * np.sqrt(dt)) + dividend_yield
                                      * self.stock_price * norm.cdf(d1) - interest_rate
                                      * self.strike_price1 * discount * norm.cdf(d2))

            bs_european_call_vega = (self.stock_price * y_discount *
                                     norm.pdf(d1) * np.sqrt(dt))
            bs_european_call_gamma = y_discount * norm.pdf(d1) / (self.stock_price *
                                                                  volatility * np.sqrt(dt))
            bs_european_call_rho = self.strike_price1 * dt * discount * norm.cdf(d2)

            return (bs_european_call_price, bs_european_call_delta, bs_european_call_theta, bs_european_call_vega,
                    bs_european_call_gamma, bs_european_call_rho)
        elif flag == 'put':
            bs_european_put_price = (self.strike_price1 * discount * norm.cdf(-d2) -
                                     self.stock_price * y_discount * norm.cdf(-d1))
            bs_european_put_delta = - y_discount * (1 - norm.cdf(d1))
            bs_european_put_theta = (- (self.stock_price * norm.pdf(d1) * volatility
                                        * y_discount) / (2 * np.sqrt(dt)) - dividend_yield
                                     * self.stock_price * norm.cdf(-d1) + interest_rate
                                     * self.strike_price1 * discount * norm.cdf(-d2))
            bs_european_put_vega = (self.stock_price * y_discount *
                                    norm.pdf(d1) * np.sqrt(dt))
            bs_european_put_gamma = y_discount * norm.pdf(d1) / (self.stock_price *
                                                                 volatility * np.sqrt(dt))
            bs_european_put_rho = -self.strike_price1 * dt * discount * norm.cdf(-d2)

            return (bs_european_put_price, bs_european_put_delta, bs_european_put_theta, bs_european_put_vega,
                    bs_european_put_gamma, bs_european_put_rho)


