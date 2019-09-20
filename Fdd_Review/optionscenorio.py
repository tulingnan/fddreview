import pandas as pd
import numpy as np
import optionpricing as op


class optionscenorio(subject):
    def __init__(self, S, K,sigma, T, r, q,flag):
        self.S = S
        self.K = K
        self.sigma = sigma
        self.T = T
        self.r = r
        self.q = q
        self.flag = flag
    def delta_vega(self,delta_range=list(np.linspace(-0.1,0.1,21)),
                   vega_range=[-0.1,0,0.1]):
        data = []