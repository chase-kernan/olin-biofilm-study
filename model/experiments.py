from pathlib import Path
from itertools import product
from collections import Iterable, Mapping

import json
import pandas as pd
import numpy as np

def from_plan(path):
    def parse_value(value):
        try:
            return np.arange(value['from'], value['to'], value['num'])
        except TypeError:
            return value

    def parse_json_plan(json_plan):
        plan = json_plan.copy()
        plan['specs'] = { param: parse_value(value) 
                          for param, value in plan['specs'].items() }
        return plan

    with path.open('r') as json_file:
        return Experiment(**parse_json_plan(json.load(json_file)))


def cartesian_product(**params):
    params = { name: value if isinstance(value, Iterable) else [value] 
               for name, value in params.items() }
    return map(dict, product(*([(name, value) for value in values]
                               for name, values in params.items())))


class Experiment:

    def __init__(self, name="experiment", runs_per_spec=5, specs={}):
        self.name = name
        self.runs_per_spec = runs_per_spec
        self.specs = specs

    @property
    def expanded_specs(self):
        return pd.DataFrame(list(cartesian_product(**self.specs)))

    def data_file(self, parent_dir):
        return parent_dir / "{}.hdf5".format(self.name)
