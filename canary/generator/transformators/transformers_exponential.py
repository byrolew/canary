from abc import ABC
from copy import deepcopy

import numpy as np

from .base import Transformer


class TransformerExponential(Transformer, ABC):
    def __init__(self):
        super(TransformerExponential, self).__init__(['exponential', 'count'])

    # def transform(self, point_dict, y):
    #     raise NotImplementedError


class AddMoveTransformer(TransformerExponential):
    def __init__(self, shift=None, change_date=None):
        """anomaly"""
        super(AddMoveTransformer, self).__init__()
        self.shift = shift
        self.change_date = change_date

    def transform(self, point_dict, y):
        if self.change_date is None:
            self.change_date = np.random.choice(list(point_dict['data'].keys()))
        if self.shift is None:
            self.shift = np.random.uniform(-0.8, 0.8)

        y_copy = deepcopy(y)
        points = point_dict['data'][self.change_date]
        points = abs(np.array(points) * (1 + self.shift))
        point_dict['data'][self.change_date] = points
        if y is not None:
            y_copy[self.change_date] = 1
            return point_dict, y_copy
        return point_dict


class AddToSomeBucketSmoothTransformer(TransformerExponential):
    def __init__(self, percentage=None, mean=None, std=None, change_date=None):
        """anomaly"""
        super(AddToSomeBucketSmoothTransformer, self).__init__()
        self.percentage = percentage
        self.mean = mean
        self.std = std
        self.change_date = change_date

    def transform(self, point_dict, y):
        y_copy = deepcopy(y)
        if self.change_date is None:
            self.change_date = np.random.choice(list(point_dict['data'].keys()))
        points = point_dict['data'][self.change_date]
        if self.mean is None:
            self.mean = np.random.uniform(low=0, high=1) * max(point_dict['buckets'])
        if self.std is None:
            self.std = np.random.uniform(low=0, high=1) * self.mean
        if self.percentage is None:
            self.percentage = np.random.uniform(0.1, 0.4)

        shape = (self.mean / self.std) ** 2
        scale = self.mean / shape
        points = [np.random.gamma(shape, scale) if
                  np.random.binomial(1, self.percentage) else p for p in points]
        point_dict['data'][self.change_date] = points
        if y is not None:
            y_copy[self.change_date] = 1
            return point_dict, y_copy
        return point_dict


class AddAnotherDistTransformer(TransformerExponential):
    def __init__(self, mean=None, std=None, change_date=None):
        """anomaly"""
        super(AddAnotherDistTransformer, self).__init__()
        self.mean = mean
        self.std = std
        self.change_date = change_date

    def transform(self, point_dict, y):
        y_copy = deepcopy(y)
        if self.change_date is None:
            self.change_date = np.random.choice(list(point_dict['data'].keys()))
        if self.mean is None:
            self.mean = np.random.uniform(low=0, high=1) * max(point_dict['buckets'])
        if self.std is None:
            self.std = np.random.uniform(low=0.3, high=1) * self.mean
        shape = (self.mean / self.std) ** 2
        scale = self.mean / shape
        points = point_dict['data'][self.change_date]
        points = np.random.gamma(shape, scale, len(points))
        point_dict['data'][self.change_date] = points
        if y is not None:
            y_copy[self.change_date] = 1
            return point_dict, y_copy
        return point_dict


class AddExpNoiseTransformer(TransformerExponential):
    def __init__(self, percentage=None):
        """not an anomaly"""
        super(AddExpNoiseTransformer, self).__init__()
        self.percentage = percentage

    def transform(self, point_dict, y):
        if self.percentage is None:
            self.percentage = np.random.uniform(0, 0.2)
        for date, points in point_dict['data'].items():
            points = [np.random.exponential(abs(p)) if
                      np.random.binomial(1, self.percentage) else p for p in points]
            point_dict['data'][date] = points
        if y is not None:
            return point_dict, y
        return point_dict


class AddTrendTransformer(TransformerExponential):
    def __init__(self, alpha=None):
        """not an anomaly, works on whole data"""
        super(AddTrendTransformer, self).__init__()
        self.alpha = alpha

    def transform(self, point_dict, y):
        if self.alpha is None:
            self.alpha = np.random.uniform(-0.001, 0.001)
        for i, (date, points) in enumerate(sorted(point_dict['data'].items())):
            trend = i * self.alpha
            points = np.array(points) * (1 + trend)
            point_dict['data'][date] = points
        if y is not None:
            return point_dict, y
        return point_dict


class AddWeekSeasonalityTransformer(TransformerExponential):
    def __init__(self, alpha=None):
        """not an anomaly, works on whole data"""
        super(AddWeekSeasonalityTransformer, self).__init__()
        self.alpha = alpha

    def transform(self, point_dict, y):
        if self.alpha is None:
            self.alpha = np.random.uniform(0, 0.1)
        week = []
        for i in range(7):
            week.append(np.random.uniform(-1, 1))
        for i, (date, points) in enumerate(sorted(point_dict['data'].items())):
            week_season = (week[i % 7]) * self.alpha
            points = np.array(points) * (1 + week_season)
            point_dict['data'][date] = points
        if y is not None:
            return point_dict, y
        return point_dict
