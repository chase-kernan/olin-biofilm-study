from pathlib import Path
from itertools import product
from collections import Iterable, Mapping

import json
import pandas as pd
import numpy as np

def load_plan(path):
    with path.open('r') as json_file:
        return Plan.from_json(json.load(json_file))

class Plan:
    @classmethod
    def from_json(cls, json_plan):
        def parse_value(value):
            try:
                return np.arange(value['from'], value['to'], value['num'])
            except TypeError:
                return value
            
        return cls(name=json_plan['name'],
                   runs_per_spec=json_plan['runs_per_spec'],
                   specs={ param: parse_value(value)
                           for param, value in json_plan['specs'].items() })

    def __init__(self, name="experiment", runs_per_spec=5, specs={}):
        self.name = name
        self.runs_per_spec = runs_per_spec
        self.specs = specs

    @property
    def expanded_specs(self):
        return pd.DataFrame(list(_cartesian_product(**self.specs)))

    def experiment_file(self, parent_dir):
        return parent_dir / "{}.hdf5".format(self.name)


def _cartesian_product(**params):
    params = { name: value if isinstance(value, Iterable) else [value] 
               for name, value in params.items() }
    return map(dict, product(*([(name, value) for value in values]
                               for name, values in params.items())))
